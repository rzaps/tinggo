from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration with simplified password validation
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'input input-bordered w-full'})
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'})
    )
    role = forms.ChoiceField(
        choices=User.UserRole.choices,
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'input input-bordered w-full'})
        self.fields['password2'].widget.attrs.update({'class': 'input input-bordered w-full'})
        
        # Упрощаем сообщения об ошибках пароля
        self.fields['password1'].help_text = _("Password must be at least 6 characters long.")
        self.fields['password2'].help_text = _("Enter the same password as before, for verification.")
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1 and len(password1) < 6:
            raise ValidationError(
                _("Password must be at least 6 characters long."),
                code='password_too_short',
            )
        return password1


class CustomUserChangeForm(UserChangeForm):
    """
    Custom form for user profile editing
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'bio', 'country', 'city', 'language')


class UserProfileForm(forms.ModelForm):
    """
    Form for extended user profile
    """
    class Meta:
        model = UserProfile
        fields = ('website', 'instagram', 'facebook', 'twitter', 'business_name', 'business_description')
        widgets = {
            'website': forms.URLInput(attrs={'class': 'input input-bordered w-full'}),
            'instagram': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'facebook': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'twitter': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'business_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'business_description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 4}),
        }


class UserAvatarForm(forms.ModelForm):
    """
    Form for user avatar upload
    """
    class Meta:
        model = User
        fields = ('avatar',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'})
        } 