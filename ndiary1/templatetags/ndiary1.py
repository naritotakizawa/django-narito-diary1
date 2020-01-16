import html
from urllib import parse
from django import template
from django.db.models import Count
from django.shortcuts import resolve_url
from django.template.defaultfilters import stringfilter
from django.utils.html import *
from django.utils.safestring import mark_safe
from ndiary1.models import Diary, Category
from ndiary1.forms import DiarySearchForm

register = template.Library()


@keep_lazy_text
def _urlize2(text, trim_url_limit=None, nofollow=False, autoescape=False):
    """
    Convert any URLs in text into clickable links.
    Works on http://, https://, www. links, and also on links ending in one of
    the original seven gTLDs (.com, .edu, .gov, .int, .mil, .net, and .org).
    Links can have trailing punctuation (periods, commas, close-parens) and
    leading punctuation (opening parens) and it'll still do the right thing.
    If trim_url_limit is not None, truncate the URLs in the link text longer
    than this limit to trim_url_limit - 1 characters and append an ellipsis.
    If nofollow is True, give the links a rel="nofollow" attribute.
    If autoescape is True, autoescape the link text and URLs.
    """
    safe_input = isinstance(text, SafeData)

    def trim_url(x, limit=trim_url_limit):
        if limit is None or len(x) <= limit:
            return x
        return '%s…' % x[:max(0, limit - 1)]

    def trim_punctuation(lead, middle, trail):
        """
        Trim trailing and wrapping punctuation from `middle`. Return the items
        of the new state.
        """
        # Continue trimming until middle remains unchanged.
        trimmed_something = True
        while trimmed_something:
            trimmed_something = False
            # Trim wrapping punctuation.
            for opening, closing in WRAPPING_PUNCTUATION:
                if middle.startswith(opening):
                    middle = middle[len(opening):]
                    lead += opening
                    trimmed_something = True
                # Keep parentheses at the end only if they're balanced.
                if (middle.endswith(closing) and
                        middle.count(closing) == middle.count(opening) + 1):
                    middle = middle[:-len(closing)]
                    trail = closing + trail
                    trimmed_something = True
            # Trim trailing punctuation (after trimming wrapping punctuation,
            # as encoded entities contain ';'). Unescape entities to avoid
            # breaking them by removing ';'.
            middle_unescaped = html.unescape(middle)
            stripped = middle_unescaped.rstrip(TRAILING_PUNCTUATION_CHARS)
            if middle_unescaped != stripped:
                trail = middle[len(stripped):] + trail
                middle = middle[:len(stripped) - len(middle_unescaped)]
                trimmed_something = True
        return lead, middle, trail

    def is_email_simple(value):
        """Return True if value looks like an email address."""
        # An @ must be in the middle of the value.
        if '@' not in value or value.startswith('@') or value.endswith('@'):
            return False
        try:
            p1, p2 = value.split('@')
        except ValueError:
            # value contains more than one @.
            return False
        # Dot must be in p2 (e.g. example.com)
        if '.' not in p2 or p2.startswith('.'):
            return False
        return True

    words = word_split_re.split(str(text))
    for i, word in enumerate(words):
        if '.' in word or '@' in word or ':' in word:
            # lead: Current punctuation trimmed from the beginning of the word.
            # middle: Current state of the word.
            # trail: Current punctuation trimmed from the end of the word.
            lead, middle, trail = '', word, ''
            # Deal with punctuation.
            lead, middle, trail = trim_punctuation(lead, middle, trail)

            # Make URL we want to point to.
            url = None
            nofollow_attr = ' rel="nofollow"' if nofollow else ''
            if simple_url_re.match(middle):
                url = smart_urlquote(html.unescape(middle))
            elif simple_url_2_re.match(middle):
                url = smart_urlquote('http://%s' % html.unescape(middle))
            elif ':' not in middle and is_email_simple(middle):
                local, domain = middle.rsplit('@', 1)
                try:
                    domain = punycode(domain)
                except UnicodeError:
                    continue
                url = 'mailto:%s@%s' % (local, domain)
                nofollow_attr = ''

            # Make link.
            if url:
                trimmed = trim_url(middle)
                if autoescape and not safe_input:
                    lead, trail = escape(lead), escape(trail)
                    trimmed = escape(trimmed)

                # 画像だった場合
                if url.endswith(('.png', '.PNG', '.bmp', '.BMP', '.jpg', '.JPG', '.jpeg', '.JPEG', '.gif', '.GIF')):
                    middle = '<a href="%s"%s><img src="%s"></a>' % (escape(url), nofollow_attr, escape(url))

                # Youtubeのリンクだった場合
                elif url.startswith('https://www.youtube.com/watch?v='):
                    video_id = url.split('=')[-1]
                    middle = '<iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' % video_id

                # 通常のリンク
                else:
                    middle = '<a href="%s"%s>%s</a>' % (escape(url), nofollow_attr, trimmed)
                words[i] = mark_safe('%s%s%s' % (lead, middle, trail))
            else:
                if safe_input:
                    words[i] = mark_safe(word)
                elif autoescape:
                    words[i] = escape(word)
        elif safe_input:
            words[i] = mark_safe(word)
        elif autoescape:
            words[i] = escape(word)
    return ''.join(words)


@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def urlize2(value, autoescape=True):
    return mark_safe(_urlize2(value, nofollow=True, autoescape=autoescape))


@register.inclusion_tag('ndiary1/includes/month_links.html')
def render_month_links():
    return {
        'dates': Diary.objects.published().dates('created_at', 'month', order='DESC'),
    }


@register.inclusion_tag('ndiary1/includes/category_links.html')
def render_category_links():
    return {
        'category_list': Category.objects.annotate(diary_count=Count('diary'))
    }


@register.inclusion_tag('ndiary1/includes/search_form.html')
def render_search_form(request):
    if hasattr(request, 'form'):
        form = request.form
    else:
        form = DiarySearchForm(request.GET)

    return {'search_form': form}


@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータの一部を置き換える。"""
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()


@register.simple_tag
def get_return_link(request):
    top_page = resolve_url('ndiary1:list')
    referer = request.environ.get('HTTP_REFERER')
    # URL直接入力やお気に入りアクセスのときはリファラがないので、トップぺージに戻す
    if referer:
        # リファラがある場合、前回ページが自分のサイト内であれば、そこに戻す。
        parse_result = parse.urlparse(referer)
        if request.get_host() == parse_result.netloc:
            return referer
    return top_page
