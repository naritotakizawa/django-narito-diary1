# django-narito-diary1
Django製の日記サイト。https://narito.ninja/diaries/

## 動作環境
Django2.2以上

## 使い方
インストールする。
```
pip install https://github.com/naritotakizawa/django-narito-diary1/archive/master.tar.gz
```

`settings.py`に追加する。
```python
INSTALLED_APPS = [
    'ndiary1.apps.Ndiary1Config',
    ...
    ...
]
```

`urls.py`に追加する。
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ndiary1.urls')),
]
```

マイグレートを行います。
```
python manage.py migrate
```

`ndiary1/base_site.html`を上書きすることで、日記サイト内のタイトル等の情報を上書きできます。上書き例です。
```html
{% extends 'ndiary1/base.html' %}

{% block meta_title %}なりと日記{% endblock %}
{% block meta_description %}なりとの日記帳です。とりとめない呟きや、感想、思ったことを書いています。毒にも薬にもならないでしょう。{% endblock %}

{% block title %}なりと日記{% endblock %}
{% block subtitle %}© 2019 Narito Takizawa.{% endblock %}

{% block link %}
    <li><a href="https://twitter.com/toritoritorina/" target="_blank">Twitter</a></li>
    <li><a href="https://github.com/naritotakizawa/" target="_blank">Github</a></li>
    <li><a href="https://narito.ninja/blog/" target="_blank">ブログ</a></li>
    <li><a href="https://narito.ninja/" target="_blank">ポートフォリオ</a></li>
    <li>
        <a href="http://www.amazon.co.jp/registry/wishlist/2ZCE9KHVM7FRA/ref=cm_sw_r_tw_ws_f.aTzbDCX47K6" target="_blank">欲しいもの</a>
    </li>
    <li><a href="mailto:toritoritorina@gmail.com" target="_blank">メール</a></li>
    <li><a href="{% url 'ndiary1:rss' %}" target="_blank">RSS</a></li>
    <li><a href="https://github.com/naritotakizawa/django-narito-diary1/" target="_blank">ソースコード</a></li>
{% endblock %}

{% block extrahead %}
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-72333380-3"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
    
        function gtag() {
            dataLayer.push(arguments);
        }
    
        gtag('js', new Date());
    
        gtag('config', 'UA-72333380-3');
    </script>
  
    <!-- Google Ads -->
    <script data-ad-client="ca-pub-5235456993770661" async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
{% endblock %}
```

日記は、Django管理サイトで次のように投稿します。URLは、画像やYoutubeリンクだった場合は自動的に変換されます。

![画像投稿の様子](https://narito.ninja/media/%E3%82%AD%E3%83%A3%E3%83%97%E3%83%81%E3%83%A3_nwDgFOt.PNG)