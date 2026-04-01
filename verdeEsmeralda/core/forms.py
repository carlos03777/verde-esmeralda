from django import forms
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox


class ContactoForm(forms.Form):

    nombre = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Tu nombre"
        }),
        error_messages={
            "required": "Por favor ingresa tu nombre"
        }
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Tu email"
        }),
        error_messages={
            "required": "Por favor ingresa tu email",
            "invalid": "Ingresa un email válido"
        }
    )

    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Escribe tu mensaje...",
            "rows": 5
        }),
        error_messages={
            "required": "El mensaje no puede estar vacío"
        }
    )

    # 🔥 ANTISPAM
    # captcha = ReCaptchaField(
    #     widget=ReCaptchaV2Checkbox(),
    #     error_messages={
    #         "required": "Confirma que no eres un robot"
    #     }
    # )

    # ======================================
    # VALIDACIONES PERSONALIZADAS
    # ======================================

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")

        if len(nombre) < 3:
            raise forms.ValidationError("El nombre es muy corto")

        return nombre

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get("mensaje")

        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje es demasiado corto")

        return mensaje