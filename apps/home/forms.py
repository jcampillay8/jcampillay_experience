from django import forms
from django.core.validators import RegexValidator

class ContactForm(forms.Form):

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener el formato: '+999999999'. Se permiten hasta 15 dígitos."
    )
    name = forms.CharField(label="Nombre", required=True, widget=forms.TextInput(
        attrs={ 'type':'text','class':'form-control', 'id':'floatingInput', 'placeholder':'Enter Name*'}
    ), min_length=10, max_length=1000)
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={ 'type':'text','class':'form-control', 'id':'floatingEmail', 'placeholder':'Enter Email*'}
    ), min_length=3, max_length=100)
    phone = forms.CharField(validators=[phone_regex], label="Phone", required=True, widget=forms.TextInput(
        attrs={ 'type':'text','class':'form-control', 'id':'floatingPassword', 'placeholder':'Enter Phone*'}
    ), min_length=3, max_length=100)
    content = forms.CharField(label="Contenido", required=True, widget=forms.Textarea(
        attrs={ 'type':'text','class':'form-control', 'rows': 3, 'id':'floatingMessage', 'placeholder':'Enter Message*', 'style':'height: 205px'}
    ), min_length=10, max_length=1000)
