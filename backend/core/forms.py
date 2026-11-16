from django import forms
from .models import Perfil, Instalacion, Horario, Reserva, Bloqueo


# UD4.3a - Formulario compartido por crear y actualizar.
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'



# UD4.3a - Formulario compartido por crear y actualizar.
class InstalacionForm(forms.ModelForm):
    class Meta:
        model = Instalacion
        fields = '__all__'



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



# UD4.3a - Formulario compartido por crear y actualizar.
class BloqueoForm(forms.ModelForm):
    class Meta:
        model = Bloqueo
        fields = '__all__'
