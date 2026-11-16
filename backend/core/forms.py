from django import forms
from .models import Perfil, Instalacion, Horario, Reserva, Bloqueo


# UD4.3a - Formulario compartido por crear y actualizar.
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'

    # UD4.3c - Validacion del formulario.
    def clean(self):
        cleaned_data = super().clean()
        alta = cleaned_data.get('fecha_alta')
        caducidad = cleaned_data.get('fecha_caducidad')
        if alta and caducidad and caducidad < alta:
            raise forms.ValidationError('La fecha de caducidad no puede ser anterior a la fecha de alta.')
        return cleaned_data



# UD4.3a - Formulario compartido por crear y actualizar.
class InstalacionForm(forms.ModelForm):
    class Meta:
        model = Instalacion
        fields = '__all__'

    # UD4.3c - Validacion del formulario.
    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad <= 0:
            raise forms.ValidationError('La capacidad debe ser mayor que cero.')
        return capacidad



# UD4.3a - Formulario compartido por crear y actualizar.
class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'



# UD4.3a - Formulario compartido por crear y actualizar.
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

    # UD4.3c - Validacion del formulario.
    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('hora_inicio')
        fin = cleaned_data.get('hora_fin')
        if inicio and fin and fin <= inicio:
            raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')
        return cleaned_data



# UD4.3a - Formulario compartido por crear y actualizar.
class BloqueoForm(forms.ModelForm):
    class Meta:
        model = Bloqueo
        fields = '__all__'
