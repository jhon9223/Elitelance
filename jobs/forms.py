from django import forms
from .models import Job, Proposal


# =========================
# Shared Tailwind Styling
# =========================

BASE_INPUT_CLASS = """
w-full px-4 py-3 rounded-xl
bg-gray-900 text-white
border border-gray-700
focus:outline-none focus:ring-2 focus:ring-purple-500
transition
"""


# =========================
# Job Create Form
# =========================

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['title', 'description', 'budget', 'category', 'deadline']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Enter job title'
            }),
            'description': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
                'rows': 6,
                'placeholder': 'Describe the job in detail'
            }),
            'budget': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Enter budget amount'
            }),
            'category': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'e.g. Web Development, Design, AI'
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASS
            }),
        }


# =========================
# Proposal Submit Form
# =========================

class ProposalForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = ['bid_amount', 'cover_letter']

        widgets = {
            'bid_amount': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Enter your bid amount'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
                'rows': 6,
                'placeholder': 'Write your cover letter...'
            }),
        }
