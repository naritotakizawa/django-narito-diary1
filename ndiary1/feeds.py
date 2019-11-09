from django.contrib.syndication.views import Feed
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from .models import Diary


class LatestDiaryFeed(Feed):
    """最新日記のフィード。"""
    title = 'My Diary - Narito Takizawa'
    description = 'なりとの日記帳の最新情報'
    link = reverse_lazy('ndiary1:list')

    def items(self):
        return Diary.objects.published().select_related('category')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text[:100]

    def item_link(self, item):
        return resolve_url('ndiary1:detail', pk=item.pk)

    def item_pubdate(self, item):
        return item.created_at

    def item_categories(self, item):
        return [item.category]
