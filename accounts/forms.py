import uuid
from extra.forms import BaseForm
from models import *
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django import forms

def generate_username():
  """
  Generate a random and unique username using the uuid library
  Also consider uniqueness by comparing with existing user names in db.
  """
  username = uuid.uuid4().hex[:30]
  try:
    while True:
      User.objects.get(username=username)
      username = uuid.uuid4().hex[:30]
  except User.DoesNotExist:
    pass
  return username

class UserInfoForm(forms.ModelForm):
  first_name = forms.CharField(max_length=30, required=False)
  last_name = forms.CharField(max_length=30, required=False)
  location = forms.CharField(max_length=100, required=False)
          
  class Meta: 
    model = User
    fields = ('first_name', 'last_name', 
              'birthday', 'mobile_number', 'location')

  def __init__(self, *args, **kwargs):
    super(UserInfoForm, self).__init__(*args, **kwargs)
    self.fields['first_name'].initial = self.instance.user.first_name
    self.fields['last_name'].initial = self.instance.user.last_name
    
  def save(self, user, commit=True): 
    """Overridden method to update the user object fields too."""
    profile = super(UserInfoForm, self).save()
    cleaned_data = self.cleaned_data
    profile.user.first_name = cleaned_data['first_name'].title()
    profile.user.last_name = cleaned_data['last_name'].title()
    profile.user.save()
    return profile


class LoginForm(AuthenticationForm):
  username = forms.EmailField(
    widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email'}))
  password = forms.CharField(
    widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  error_messages = {
    'invalid_login': ("Please enter a correct email and password."
                      "Note that both fields are case-sensitive."),
    'inactive': "This account is inactive."
  }

class UserAddressForm(BaseForm):
     class Meta:
         model = UserAddress
         fields = '__all__'   
         exclude = ('user',) 


class ContactForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-block form-control input-md','placeholder':'subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control-block form-control input-md margin-top','placeholder':'message'}))
    sender = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control-block form-control input-md','placeholder':'sender'}))


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2
