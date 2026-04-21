from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form. New churches get their own organization."""
    
    church_name = forms.CharField(
        max_length=200,
        required=True,
        label='Church / Organization name',
        help_text='The name of your church or organization. Your data will be kept separate from other churches.',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Grace Baptist Church'})
    )
    
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. Enter your first name.'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. Enter your last name.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'church_name', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Required. At least 8 characters.'
        self.fields['password2'].help_text = 'Required. Enter the same password as before, for verification.'
