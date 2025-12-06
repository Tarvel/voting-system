from django import forms
from django.core.validators import FileExtensionValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )


class CandidateCsvUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )
