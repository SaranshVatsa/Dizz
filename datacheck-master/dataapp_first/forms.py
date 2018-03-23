from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class UrlForm(forms.Form):
    url = forms.CharField(label='url', max_length=10000)