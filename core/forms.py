from django import forms
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model

# import logging
# logger = logging.getLogger('__name__')

class PersonnalInformationForm(forms.Form):
    # first_name, last_name, email
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john.doe@example.com'}))

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
            queryset = get_user_model().objects.exclude(pk=self.user.pk)
        else:
            queryset = get_user_model().objects.all()

        if queryset.filter(email=email).exists():
            raise forms.ValidationError(_("This email is already taken.","User Profile"))
        
        return email
    
    def save(self):
        if self.user:
            # logger.debug(f"Attempting to update user with id, first_name, last_name as {self.user.id} {self.user.first_name} {self.user.last_name}")
            edited_user = get_user_model().objects.get(id=self.user.id)
            edited_user.first_name = self.cleaned_data.get('first_name')
            edited_user.last_name = self.cleaned_data.get('last_name')
            edited_user.email = self.cleaned_data.get('email')
            edited_user.save()

    
    
