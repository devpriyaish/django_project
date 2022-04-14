from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from users.models import Profile


class UserRegisterForm(UserCreationForm):           # UserCreationForm in auth/forms.py >> ModelForm in auth/forms.py
                                                    # >> # BaseModelForm in forms/models.py >> BaseForm in
                                                    # form/forms.py >>
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:                                     # If an object is created using child class means inner class
                                                    # then the object can also be used by parent class
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
    CHOICES = [('MALE', 'Male'),
               ('FEMALE', 'Female'),
               ('OTHERS', 'Others')]
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Profile
        fields = ['gender', 'mobile_number', 'date_of_birth', 'country', 'image']
        widgets = {'date_of_birth': DateInput()}
