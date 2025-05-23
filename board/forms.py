from django import forms
from .models import Ad, Response, Newsletter
from django.core.exceptions import ValidationError
from django_ckeditor_5.widgets import CKEditor5Widget


class AdForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="extends"))

    class Meta:
        model = Ad
        fields = ["title", "category", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].help_text = "Выберите категорию для объявления."
        self.fields["category"].widget.attrs.update({"class": "category-class"})


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Введите ваш отклик..."}
            ),
        }

    def clean_content(self):
        content = self.cleaned_data["content"]
        if not content or len(content) < 10:
            raise forms.ValidationError("Отклик должен содержать хотя бы 10 символов.")
        return content


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["subject", "message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Введите текст рассылки"}
            ),
            "subject": forms.TextInput(attrs={"placeholder": "Тема письма"}),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get("subject", "")
        if not subject.strip():
            raise ValidationError("Поле темы не может быть пустым.")
        return subject
