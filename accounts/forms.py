from django import forms
from .models import EmployeeProfile
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
        

class EmployeeCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = EmployeeProfile
        fields = ['username', 'email', 'phone', 'position', 'photo', 'address', 'birth_date']