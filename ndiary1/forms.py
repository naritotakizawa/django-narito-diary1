from django import forms
from django.core.files.storage import default_storage


class DiarySearchForm(forms.Form):
    """検索フォーム。"""
    key_word = forms.CharField(
        label='検索キーワード',
        required=False,
    )


class FileUploadForm(forms.Form):
    """ファイルのアップロードフォーム"""
    file = forms.FileField()

    def save(self):
        upload_file = self.cleaned_data['file']
        file_name = default_storage.save(upload_file.name, upload_file)
        file_url = default_storage.url(file_name)
        return file_url
