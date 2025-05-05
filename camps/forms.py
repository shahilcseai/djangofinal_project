from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Camp, CampRegistration

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CampRegistrationForm(forms.ModelForm):
    class Meta:
        model = CampRegistration
        fields = []  # No fields needed as we'll set camp and user in the view

    def __init__(self, *args, **kwargs):
        self.camp = kwargs.pop('camp', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.camp = self.camp
        instance.user = self.user
        if commit:
            instance.save()
        return instance

class CampSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search camps...'}))
    category = forms.ChoiceField(required=False, choices=[
        ('', 'All Categories'),
        ('general', 'General'),
        ('emergency', 'Emergency'),
        ('special', 'Special Drive'),
    ])
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'})) 