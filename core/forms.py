from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# from .models import MailUser

User = get_user_model()

class MailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "votre@email.com",
                "autocomplete": "email",
            }
        )
    )

class MailUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "votre@email.com",
            })
        )

class MailPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "votre@email.com",
                "autocomplete": "email",
            })
        )

# Generate a password form for the activation mail
class MailUserActivationForm(forms.Form):
    password1 = forms.CharField(
        label=_("password1"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label=_("password2"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", _("Matching password error."))

        if password1:
            try:
                validate_password(password1)
            except ValidationError as error:
                self.add_error("password1", error)

        return cleaned_data

class MailUserChangeForm(forms.Form):
    first_name = forms.CharField(max_length=50, label=pgettext_lazy("User Profile","Firstname"),  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prénom'}))
    last_name = forms.CharField(max_length=50, required=False, label=pgettext_lazy("User Profile","Lastname"), widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}))

    class Meta:
        model = User
        fields = ("first_name","last_name","email")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # pop the user from the kwargs
        super().__init__(*args, **kwargs)
        # populate field as default
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.user:
            if self.user.email == email:
                return email
            queryset = User.objects.exclude(pk=self.user.pk)
        else:
            queryset = User.objects.all()

        if queryset.filter(email=email).exists():
            raise forms.ValidationError(pgettext_lazy("User Profile","This email is already taken."))
        
        return email
    
    def save(self):
        if self.user:
            edited_user = get_user_model().objects.get(id=self.user.id)
            edited_user.first_name = self.cleaned_data.get('first_name')
            edited_user.last_name = self.cleaned_data.get('last_name')
            edited_user.email = self.cleaned_data.get('email')
            edited_user.save()

    
    
