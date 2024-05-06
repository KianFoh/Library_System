from django import forms

class ContactForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)