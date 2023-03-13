from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'topic',
           'rating',
           'text',
           'category',
       ]

   def clean(self):
       cleaned_data = super().clean()
       text = cleaned_data.get("text")
       if text is not None and len(text) < 20:
           raise ValidationError({"text" : "Текст не может быть менее 20 символов."})

       topic = cleaned_data.get("topic")
       if topic == text:
           raise ValidationError("Название новости не должно быть индентично тексту.")

       return cleaned_data

