from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Rating, RecipeIngredient, Recipe, RecipeStep


class SignupForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Form for user login"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Form for user profile updates"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    """Form for recipe reviews"""
    class Meta:
        model = Review
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title',
                'maxlength': '255'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review...',
                'rows': 5
            }),
        }


class RatingForm(forms.ModelForm):
    """Form for recipe ratings"""
    class Meta:
        model = Rating
        fields = ('score',)
        widgets = {
            'score': forms.RadioSelect(choices=[(i, f'{i} Stars') for i in range(1, 6)],
                                       attrs={'class': 'form-check-input'})
        }


class AddRecipeForm(forms.ModelForm):
    """Form for creating/editing recipes"""
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'prep_time', 'cook_time', 'servings', 
                  'difficulty', 'category', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Recipe description'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Recipe image URL'}),
        }


class RecipeIngredientForm(forms.ModelForm):
    """Form for adding ingredients to recipes"""
    ingredient_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient name'})
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'unit', 'notes')
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., chopped, minced (optional)'}),
        }


class RecipeStepForm(forms.ModelForm):
    """Form for adding cooking steps"""
    class Meta:
        model = RecipeStep
        fields = ('instruction', 'time_minutes')
        widgets = {
            'instruction': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Step instructions'}),
            'time_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Time (minutes, optional)'}),
        }

    """Form for recipe ratings"""
    class Meta:
        model = Rating
        fields = ('score',)
        widgets = {
            'score': forms.RadioSelect(choices=[(i, f'{i} Stars') for i in range(1, 6)],
                                       attrs={'class': 'form-check-input'})
        }


class AddRecipeForm(forms.ModelForm):
    """Form for creating/editing recipes"""
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'prep_time', 'cook_time', 'servings', 
                  'difficulty', 'category', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Recipe description'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Recipe image URL'}),
        }


class RecipeIngredientForm(forms.ModelForm):
    """Form for adding ingredients to recipes"""
    ingredient_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient name'})
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'unit', 'notes')
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., chopped, minced (optional)'}),
        }


class RecipeStepForm(forms.ModelForm):
    """Form for adding cooking steps"""
    class Meta:
        model = RecipeStep
        fields = ('instruction', 'time_minutes')
        widgets = {
            'instruction': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Step instructions'}),
            'time_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Time (minutes, optional)'}),
        }
