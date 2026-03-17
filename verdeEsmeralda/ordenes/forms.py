from django import forms
from .models import Direccion
import re


DEPARTAMENTOS = [

    ("Amazonas", "Amazonas"),
    ("Antioquia", "Antioquia"),
    ("Arauca", "Arauca"),
    ("Atlántico", "Atlántico"),
    ("Bogotá", "Bogotá"),
    ("Bolívar", "Bolívar"),
    ("Boyacá", "Boyacá"),
    ("Caldas", "Caldas"),
    ("Caquetá", "Caquetá"),
    ("Casanare", "Casanare"),
    ("Cauca", "Cauca"),
    ("Cesar", "Cesar"),
    ("Chocó", "Chocó"),
    ("Córdoba", "Córdoba"),
    ("Cundinamarca", "Cundinamarca"),
    ("Guainía", "Guainía"),
    ("Guaviare", "Guaviare"),
    ("Huila", "Huila"),
    ("La Guajira", "La Guajira"),
    ("Magdalena", "Magdalena"),
    ("Meta", "Meta"),
    ("Nariño", "Nariño"),
    ("Norte de Santander", "Norte de Santander"),
    ("Putumayo", "Putumayo"),
    ("Quindío", "Quindío"),
    ("Risaralda", "Risaralda"),
    ("San Andrés", "San Andrés"),
    ("Santander", "Santander"),
    ("Sucre", "Sucre"),
    ("Tolima", "Tolima"),
    ("Valle del Cauca", "Valle del Cauca"),
    ("Vaupés", "Vaupés"),
    ("Vichada", "Vichada"),
]


class DireccionForm(forms.ModelForm):

    nombre = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nombre de quien recibe",
            "autocomplete": "name"
        })
    )

    celular = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "3001234567",
            "pattern": "[0-9]+",
            "inputmode": "numeric",
            "autocomplete": "tel"
        })
    )

    direccion = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej: Cra 10 #20-30",
            "autocomplete": "street-address"
        })
    )

    ciudad = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ciudad",
            "autocomplete": "address-level2"
        })
    )

    departamento = forms.ChoiceField(
        choices=DEPARTAMENTOS,
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    codigoPostal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Código postal (opcional)",
            "autocomplete": "postal-code"
        })
    )

    class Meta:
        model = Direccion
        fields = [
            "nombre",
            "celular",
            "direccion",
            "ciudad",
            "departamento",
            "codigoPostal"
        ]

    # VALIDAR NOMBRE
    def clean_nombre(self):

        nombre = self.cleaned_data["nombre"]

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$", nombre):
            raise forms.ValidationError(
                "El nombre solo puede contener letras"
            )

        return nombre

    # VALIDAR CELULAR
    def clean_celular(self):

        celular = self.cleaned_data["celular"]

        if not celular.isdigit():
            raise forms.ValidationError(
                "El celular solo debe contener números"
            )

        if len(celular) != 10:
            raise forms.ValidationError(
                "El celular debe tener 10 dígitos"
            )

        if not celular.startswith("3"):
            raise forms.ValidationError(
                "El celular debe comenzar con 3"
            )

        return celular

    # VALIDAR DIRECCION
    def clean_direccion(self):

        direccion = self.cleaned_data["direccion"]

        if len(direccion) < 5:
            raise forms.ValidationError(
                "La dirección parece demasiado corta"
            )

        return direccion

    # VALIDAR CIUDAD
    def clean_ciudad(self):

        ciudad = self.cleaned_data["ciudad"]

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$", ciudad):
            raise forms.ValidationError(
                "La ciudad solo puede contener letras"
            )

        return ciudad