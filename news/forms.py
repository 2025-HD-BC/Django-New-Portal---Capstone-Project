"""
Django News Portal Forms

This module contains all the form classes for the news portal application.
It includes forms for user registration, profile editing, article submission,
publisher management, and newsletter creation.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Article, CustomUser, Publisher, Newsletter

class ArticleForm(forms.ModelForm):
    """
    Form for journalists to submit or edit news articles.
    
    Includes fields for title, content, publisher association, and optional image upload.
    Styled with Bootstrap CSS classes for consistent appearance.
    """
    class Meta:
        model = Article
        fields = ["title", "content", "publisher", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "publisher": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Headline",
            "content": "Article Body",
            "publisher": "Publisher Organization",
            "image": "Article Image (optional)"
        }

class CustomUserSignupForm(UserCreationForm):
    """
    User registration form supporting multiple user roles.
    
    Extends Django's UserCreationForm to include role selection and email field.
    Supports registration for readers, editors, journalists, and publishers.
    """
    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-select"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }
        labels = {
            "role": "Account Type"
        }
        help_texts = {
            "role": "Choose your role: Reader, Editor, Journalist, or Publisher."
        }

class ProfileEditForm(forms.ModelForm):
    """
    Form for users to update their profile information.
    
    Allows users to modify their username, email, profile image, contact number,
    and biographical information. Provides proper validation and Bootstrap styling.
    """
    class Meta:
        model = CustomUser
        fields = ["username", "email", "profile_image", "contact_number", "bio"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "contact_number": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "profile_image": "Profile Photo",
            "contact_number": "Contact Number",
            "bio": "Short Bio",
        }
        help_texts = {
            "bio": "Optional: Tell us a bit about yourself.",
        }

class PublisherForm(forms.ModelForm):
    """
    Form for creating and editing publisher organizations.
    
    Allows association of editors and journalists with publishers through
    multi-select fields. Automatically filters user choices based on appropriate roles.
    """
    class Meta:
        model = Publisher
        fields = ['name', 'editors', 'journalists']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'editors': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'journalists': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        labels = {
            "name": "Publisher Name",
            "editors": "Editors (users with edit/admin rights)",
            "journalists": "Journalists (users who can submit articles)"
        }
        help_texts = {
            "editors": "Hold Ctrl/Cmd to select multiple editors.",
            "journalists": "Hold Ctrl/Cmd to select multiple journalists."
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with role-based user filtering.
        
        Limits editor choices to users with editor/publisher roles and
        journalist choices to users with journalist role.
        """
        super().__init__(*args, **kwargs)
        # Limit choices to users of appropriate roles
        self.fields['editors'].queryset = CustomUser.objects.filter(role__in=['editor', 'publisher'])
        self.fields['journalists'].queryset = CustomUser.objects.filter(role='journalist')

class NewsletterForm(forms.ModelForm):
    """
    Form for journalists to create and submit newsletters.
    
    Provides fields for newsletter title, content, and optional publisher association.
    Automatically filters publisher choices based on the user's associations.
    """
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Newsletter Title',
            'content': 'Newsletter Body',
            'publisher': 'Publisher (Optional)',
        }
        help_texts = {
            'content': 'Write the full newsletter content here.',
            'publisher': 'Select a publisher to associate with this newsletter (optional).',
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with user-specific publisher filtering.
        
        Args:
            user: The current user, used to filter available publishers
            
        Limits publisher choices to those associated with the user if applicable,
        otherwise shows all publishers. Makes publisher field optional.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Limit publisher choices based on the user's associations
        if user and hasattr(user, 'journalist_of_publishers'):
            self.fields['publisher'].queryset = user.journalist_of_publishers.all()
        else:
            self.fields['publisher'].queryset = Publisher.objects.all()
        
        # Make publisher field optional
        self.fields['publisher'].required = False
