from django import forms

class ChatBotForm(forms.Form):
    question=forms.CharField(max_length=155)
    class Meta:
        fields=['question',]