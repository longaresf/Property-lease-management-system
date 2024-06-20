from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image


INMUEBLES = (('Casa', 'Casa'),('Departamento', 'Departamento'),('Parcela', 'Parcela'))

USUARIO = (('Arrendador', 'Arrendador'),('Arrendatario', 'Arrendatario'))

ESTADO = (('Pendiente', 'Pendiente'),('Rechazado', 'Rechazado'),('Aprobado', 'Aprobado'))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
         label = 'Usuario',
     )
    password = forms.CharField(max_length=30,
        widget=forms.PasswordInput,
         label = 'Password',
     )

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit = True):
        user = super().save()
        self.save_m2m()
        return user
    
class SearchForm(forms.Form):

    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Búsqueda por Región, Ciudad o Comuna'}), max_length=100, label='')
    
class UserForm(forms.ModelForm):
    
    tipo_user = forms.ChoiceField(
        choices=USUARIO,
         label = 'Tipo',
     )
    
    class Meta:
        model = Usuario
        fields = ('rut', 'nombres', 'apellidos', 'direccion', 'telefono', 'email', 'tipo_user', 'activo', 'usuario', 'creado_por')


class InmForm(forms.ModelForm):
    
    construido = forms.CharField(
         label = 'Área Construida',
     )
    totales = forms.CharField(
         label = 'Área Total',
     )
    banios = forms.CharField(
         label = 'Baños',
     )
    direccion = forms.CharField(
         label = 'Dirección',
     )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
         label = 'Comuna',
     )
    inmueble_tipo = forms.ChoiceField(
        choices=INMUEBLES,
         label = 'Tipo',
     )
    arriendo_mes = forms.CharField(
         label = 'Arriendo Mensual',
     )

    class Meta:
        model = Inmueble
        fields = ('nombre', 'descripcion', 'construido', 'totales', 'estacionamiento', 'habitaciones', 'banios', 'direccion', 'comuna', 'inmueble_tipo', 'arriendo_mes')
        


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class ImageForm(forms.ModelForm):
    image = MultipleFileField(label = "Imágenes")
    class Meta:
        model = Image
        fields = ['image',]

class EstatusArriendoForm(forms.ModelForm):
    
    estado = forms.ChoiceField(
        choices=ESTADO,
         label = 'Estatus Arriendo',
     )
    class Meta:
        model = Usuario_Inmueble
        fields = ['estado',]