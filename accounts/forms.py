"""
Account Forms

=== LARAVEL COMPARISON ===
These forms handle user registration and profile editing.
Like Laravel's RegisterController validation + Form Requests.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    """
    Registration form — extends Django's built-in UserCreationForm.

    Laravel equivalent:
        // In RegisterController:
        protected function validator(array $data) {
            return Validator::make($data, [
                'username' => 'required|string|max:150|unique:users',
                'email' => 'required|string|email|unique:users',
                'password' => 'required|string|min:8|confirmed',
            ]);
        }

    UserCreationForm already handles:
    - password1 and password2 (password + confirmation)
    - Password validation (length, common passwords, etc.)
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class ProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    class Meta:
        model = Profile
        fields = ['bio', 'role']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    """Form for updating basic user info (name, email)."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
