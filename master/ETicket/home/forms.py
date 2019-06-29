from django import forms
from .models import Invoice, Rate, AuthUser, Company, Paymenttype
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget


class RateForm(forms.ModelForm):
    ratename = forms.CharField(
        help_text="Hola",
        label="Nombre de tarifa",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'oninvalid':"this.setCustomValidity('Ingresa el nombre de la tarifa');",
                                      'oninput':"setCustomValidity('')"}))

    rateprice = forms.IntegerField(
        label="Precio",
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'oninvalid':"this.setCustomValidity('Ingresa el precio de la tarifa');",
                                        'oninput':"setCustomValidity('')",
                                        'step': 1}))

    ratetime = forms.IntegerField(
        help_text="Bye",
        label="Tiempo de tarifa",
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'oninvalid':"this.setCustomValidity('Ingresa el tiempo (min) de la tarifa');",
                                        'oninput':"setCustomValidity('')"}))

    class Meta:
        model = Rate
        fields = ('ratename','rateprice','ratetime')


class InvoiceForm(forms.ModelForm):
    invoicedate = forms.DateField(
        label="Fecha de factura",
        widget= forms.DateInput(attrs={"class":"form-control","readonly":"true"})
    )
    chosenrate = forms.ModelChoiceField(
        label="Tarifa",
        widget= forms.Select(attrs={"class":"form-control",
                                    "onChange":"getRateprice();",
                                    'oninvalid':"this.setCustomValidity('Elije una tarifa');",
                                    'oninput':"setCustomValidity('')"}),
        queryset = Rate.objects.all()
    )
    inithour = forms.CharField(
        label="Hora de inicio",
        widget= forms.TextInput(attrs={"class":"form-control","readonly":"true"})
    )
    endhour = forms.CharField(
        label="Hora de finalizacion",
        widget= forms.TextInput(attrs={"class":"form-control","readonly":"true"})
    )
    customerid  = forms.CharField(
        required=False,
        label="Cedula del cliente",
        widget= forms.TextInput(attrs={"class":"form-control"})
    )
    customername = forms.CharField(
        required=False,
        label="Nombre del cliente",
        widget= forms.TextInput(attrs={"class":"form-control"})
    )
    customerphone = forms.IntegerField(
        required=False,
        label="Telefono del cliente",
        widget= forms.NumberInput(attrs={"class":"form-control"})
    )
    customeraddress = forms.CharField(
        required=False,
        label="Direccion del cliente",
        widget= forms.TextInput(attrs={"class":"form-control"})
    )
    customeremail = forms.EmailField(
        required=False,
        label="Email del cliente",
        widget= forms.EmailInput(attrs={"class":"form-control"})
    )
    total = forms.DecimalField(
        decimal_places=1,
        label="Total",
        widget= forms.NumberInput(attrs={"class":"form-control","readonly":"true"})
    )
    paymenttype = forms.ModelChoiceField(
        label="Tipo de pago",
        widget=forms.Select(attrs={"class": "form-control",
                                   'oninvalid':"this.setCustomValidity('Elije un metodo de pago');",
                                    'oninput':"setCustomValidity('')"}),
        queryset=Paymenttype.objects.all()
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Cantidad",
        widget= forms.NumberInput(attrs={"class":"form-control","oninput":"calculateTotal();"})
    )

    tax = forms.IntegerField(
        min_value=0,
        initial=0,
        label="I.V",
        widget= forms.NumberInput(attrs={"class":"form-control","oninput":"calculateTotal();"})
    )

    def save(self, commit=True):
        instance = super(InvoiceForm, self).save(commit=False)
        instance.invoiceid = instance.get_invoice_id()
        instance.invoiceactive = True
        instance.save()
        return instance

    class Meta:
        model = Invoice
        fields = (
            'invoicedate',
            'chosenrate',
            'quantity',
            'paymenttype',
            'inithour',
            'endhour',
            'customerid',
            'customername',
            'customeremail',
            'customerphone',
            'customeraddress',
            'tax',
            'total',
        )


class AuthUserForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder':'Ej: jose1234',
                                      'oninvalid':"this.setCustomValidity('Debes ingresar el nombre de usuario. Ej: jose1234');",
                                      'oninput':"setCustomValidity('')"}))

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'oninvalid':"this.setCustomValidity('Debes ingresar una contraseña para el usuario');",
                                          'oninput':"setCustomValidity('')"}))

    is_superuser = forms.BooleanField(
        initial=True,
        required=False,
        label="Tiene permisos de administrador?",
        widget=forms.CheckboxInput(attrs={'class': 'form-control',
                                          'data-toggle':"toggle",
                                          'data-on':"Si",
                                          'data-off':"No",
                                          'data-offstyle':"danger",
                                          'data-onstyle':"success"}))


    is_active = forms.BooleanField(
        initial=True,
        required=False,
        label="Usuario activo?",
        widget=forms.CheckboxInput(attrs={'class': 'form-control',
                                          'checked':'true',
                                          'data-toggle':"toggle",
                                          'data-on':"Si",
                                          'data-off':"No",
                                          'data-offstyle':"danger",
                                          'data-onstyle':"success"}))

    date_joined = forms.DateTimeField(
        label="Fecha de ingreso",
        widget=forms.DateTimeInput(attrs={'class': 'form-control','type':'date'}))


    class Meta:
        model = AuthUser
        fields = (
            'username',
            'password',
            'is_superuser',
            'is_active',
            'date_joined'
        )

    def save(self, commit=True):
        instance = super(AuthUserForm, self).save(commit=False)
        company = Company.objects.get()
        instance.email = company.companyemail
        instance.password = make_password(instance.password)
        instance.save()
        return instance
    

class AuthUserUpdateForm(forms.ModelForm):
        
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder':'Ej: jose1234',
                                      'oninvalid':"this.setCustomValidity('Debes ingresar el nombre de usuario. Ej: jose1234');",
                                      'oninput':"setCustomValidity('')"}))

    is_superuser = forms.BooleanField(
        initial=True,
        required=False,
        label="Tiene permisos de administrador?",
        widget=forms.CheckboxInput(attrs={'class': 'form-control',
                                          'data-toggle': "toggle",
                                          'data-on': "Si",
                                          'data-off': "No",
                                          'data-offstyle': "danger",
                                          'data-onstyle': "success"}))


    is_active = forms.BooleanField(
        initial=True,
        required=False,
        label="Usuario activo?",
        widget=forms.CheckboxInput(attrs={'class': 'form-control',
                                          'checked': 'true',
                                          'data-toggle': "toggle",
                                          'data-on': "Si",
                                          'data-off': "No",
                                          'data-offstyle': "danger",
                                          'data-onstyle': "success"}))

    date_joined = forms.DateTimeField(
        error_messages={'required': 'Este campo es requerido'},
        label="Fecha de ingreso",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': 'true'}))

    class Meta:
        model = AuthUser
        fields = (
            'username',
            'is_superuser',
            'is_active',
            'date_joined'
        )

    def save(self, commit=True):
        instance = super(AuthUserUpdateForm, self).save(commit=False)
        instance.save()
        return instance


class CompanyForm(forms.ModelForm):
    companyid = forms.CharField(
        label="Identificacion",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'oninvalid':"this.setCustomValidity('Ingresa la identificacion de la empresa');",
                                      'oninput':"setCustomValidity('')"}))

    companyname = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'oninvalid':"this.setCustomValidity('Debes ingresar el nombre de la empresa');",
                                      'oninput':"setCustomValidity('')"}))

    companyphone = forms.CharField(
        label="Telefono",
        widget=forms.TextInput(attrs={'class': 'form-control','oninvalid':"this.setCustomValidity('Debes ingresar el telefono de la empresa');",
                                      'oninput':"setCustomValidity('')"}))

    companyaddress = forms.CharField(
        label="Direccion",
        widget=forms.Textarea(attrs={'class': 'form-control','oninvalid':"this.setCustomValidity('Debes ingresar la direccion de la empresa');",
                                      'oninput':"setCustomValidity('')"}))
    companyemail = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class":'form-control','oninvalid':"this.setCustomValidity('Debes ingresar el correo de la empresa');",
                                      'oninput':"setCustomValidity('')"})
    )

    class Meta:
        model = Company
        fields = ('companyid','companyname','companyphone','companyaddress','companyemail')