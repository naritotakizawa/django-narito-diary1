from django.db import models
from django.utils import timezone


class Category(models.Model):
    """日記のカテゴリ"""
    name = models.CharField('タイトル', max_length=255)

    def __str__(self):
        return self.name


class DiaryQuerySet(models.QuerySet):

    def published(self):
        return self.filter(created_at__lte=timezone.now())


class Diary(models.Model):
    """日記"""
    title = models.CharField('タイトル', max_length=32)
    text = models.TextField('本文')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリ')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    objects = DiaryQuerySet.as_manager()

    def __str__(self):
        return self.title
