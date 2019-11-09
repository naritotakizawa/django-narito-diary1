from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url
from .models import Diary


class DiarySitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Diary.objects.published()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return resolve_url('ndiary1:detail', pk=obj.pk)
