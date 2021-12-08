from django import forms
from django.forms import ModelForm

from authapp.forms import UserRegistrationForm, UserProfileForm
from authapp.models import User
from mainapp.models import Product, ProductCategory


class UserAdminRegistrationForm(UserRegistrationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'age', 'image')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class UserAdminProfileForm(UserProfileForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))


class ProductAdminRegistrationForm(ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity', 'category', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите имя продукта'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание товара'
        self.fields['price'].widget.attrs['placeholder'] = 'Введите цену'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Введите количество'
        self.fields['category'].widget.attrs['placeholder'] = 'Введите категорию товара'
        self.fields['image'].widget.attrs['placeholder'] = 'Добавьте каринку'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class ProductAdminProfileForm(ProductAdminRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(ProductAdminRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class CategoryUpdateFormAdmin(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateFormAdmin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

