from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, ClientProfile, FreelancerProfile


#  REGISTER FORM

class RegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Username'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Email'
        })
    )

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def clean_role(self):
        role = self.cleaned_data.get('role')

        # Prevent selecting manager via public registration
        if role == 'manager':
            raise forms.ValidationError("You cannot register as manager.")

        return role


#  LOGIN FORM

class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("Invalid username or password.")

            self.user = user

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


#  CLIENT PROFILE FORM

class ClientProfileForm(forms.ModelForm):

    class Meta:
        model = ClientProfile
        fields = ['company_name', 'company_description']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-2 focus:ring-teal-500'
            }),
            'company_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-2 focus:ring-teal-500',
                'rows': 4
            }),
        }


# 👤 FREELANCER PROFILE FORM

class FreelancerProfileForm(forms.ModelForm):

    class Meta:
        model = FreelancerProfile
        fields = [
            'skills',
            'bio',
            'hourly_rate',
            'experience',
            'portfolio_link',
        ]
        widgets = {
            'skills': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-2 focus:ring-teal-500'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-2 focus:ring-teal-500',
                'rows': 4
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-2 focus:ring-teal-500'
            }),
            'experience': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-2 focus:ring-teal-500'
            }),
            'portfolio_link': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 dark:bg-gray-800 dark:border-gray-700 focus:ring-2 focus:ring-teal-500'
            }),
        }
