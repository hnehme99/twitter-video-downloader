from django import forms
from .models import Url

class UrlForm(forms.ModelForm):
    # link = forms.CharField(max_length=10000)
    class Meta:
        model = Url
        fields = [
            'link'
        ]


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length = 50)
    email_address = forms.EmailField(max_length = 150)
    message = forms.CharField(widget = forms.Textarea, max_length=2000)
