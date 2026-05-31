from django import forms
from users.forms import validate_github_url

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Динамически добавляем классы всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            
        # Индивидуальные атрибуты
        self.fields["name"].widget.attrs["placeholder"] = "Название проекта"
        self.fields["description"].widget.attrs["rows"] = 4
        self.fields["github_url"].widget.attrs["placeholder"] = "https://github.com/..."

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        return validate_github_url(url)
