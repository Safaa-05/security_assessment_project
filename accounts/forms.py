from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control form-control-lg",
            "placeholder": "Enter your username",
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-control form-control-lg",
            "placeholder": "Enter your email",
        })

        self.fields["phone_number"].widget.attrs.update({
            "class": "form-control form-control-lg",
            "placeholder": "Enter your phone number",
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control form-control-lg",
            "placeholder": "Enter your password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control form-control-lg",
            "placeholder": "Confirm your password",
        })


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter your username",
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter your password",
            }
        ),
    )