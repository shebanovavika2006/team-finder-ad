import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


def validate_github_url(url):
    if url and "github.com" not in url.lower():
        raise forms.ValidationError("Ссылка должна вести на платформу GitHub.")
    return url


class StyleMixin:
    """Примесь для автоматического добавления классов Bootstrap ко всем полям."""
    def apply_styles(self):
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class LoginForm(forms.Form, StyleMixin):
    email = forms.EmailField(label="Электронная почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        kwargs.pop("request", None)
        
        super().__init__(*args, **kwargs)
        self.apply_styles()
        self.fields["email"].widget.attrs["placeholder"] = "email@example.com"


class RegisterForm(forms.ModelForm, StyleMixin):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm, StyleMixin):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "avatar", "about", "phone", "github_url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()
        self.fields["about"].widget.attrs["rows"] = 3
        self.fields["phone"].widget.attrs["placeholder"] = "+7XXXXXXXXXX"

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        if not phone:
            return phone

        clean_number = re.sub(r"[\s\-]", "", phone)
        if clean_number.startswith("8"):
            clean_number = "+7" + clean_number[1:]

        if not re.match(r"^\+7\d{10}$", clean_number):
            raise forms.ValidationError("Формат телефона: 8XXXXXXXXXX или +7XXXXXXXXXX.")

        if User.objects.filter(phone=clean_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот номер уже используется другим пользователем.")

        return clean_number

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url"))


class CustomPasswordChangeForm(PasswordChangeForm, StyleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()
