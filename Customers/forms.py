from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Product, Category, CustomerProfile, Order, ContactMessage


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter first name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Create a strong password'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm your password'}),
        min_length=6
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Choose a username'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your password'})
    )


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Street address, Apartment/Suite'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-input'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address', 'city', 'state', 'postal_code', 'country', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-file-input'}),
        }


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    brand = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brand / Manufacturer'}))
    discount_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': '0.00'}))
    deal_discount_percent = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 20'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Detailed product description'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-file-input'}))
    image_url = forms.URLField(max_length=800, required=False, widget=forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://images.unsplash.com/... (Online Image URL)'}))

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'brand', 'price', 'discount_price',
            'stock', 'description', 'image', 'image_url', 'status', 'featured',
            'is_deal', 'deal_discount_percent', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Available quantity in stock'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class CategoryForm(forms.ModelForm):
    image_url = forms.URLField(max_length=800, required=False, widget=forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://images.unsplash.com/...'}))

    class Meta:
        model = Category
        fields = ['name', 'icon', 'image', 'image_url', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Category Name'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'fa-laptop'}),
            'image': forms.FileInput(attrs={'class': 'form-file-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Category description'}),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'state', 'postal_code', 'country',
            'payment_method', 'order_notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Street Address & Apartment', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State / Province', 'required': True}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Postal Code', 'required': True}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Country', 'required': True}),
            'payment_method': forms.RadioSelect(attrs={'class': 'payment-radio'}),
            'order_notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Special delivery notes (optional)'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email Address', 'required': True}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Subject of message', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'Write your message here...', 'required': True}),
        }