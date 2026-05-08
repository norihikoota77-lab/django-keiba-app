from django import forms

class UploadForm(forms.Form):
    correct_file = forms.FileField()
    user_file = forms.FileField()