from django import forms
from  .models import Registration
class Registrationform(forms.ModelForm):
    class Meta:
        model= Registration
        fields =[
            'firstname',
            'lastname',
            'email',
            'password',
            'confirm_password',
        ]