from django import forms
from .models import Project
from .models import UserProfile
from django.contrib.auth.models import User

class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomUserEditForm(forms.ModelForm):
    password = forms.CharField(
        label="New Password",
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Leave blank to keep unchanged'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'age', 'qualification', 'date_of_joining', 'address', 'marital_status']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'})
        }
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'hours', 'priority', 'progress', 'status', 'members']
        widgets = {
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }