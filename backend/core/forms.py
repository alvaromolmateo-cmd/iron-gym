from django import forms
from .models import Perfil, Instalacion, Horario, Reserva, Bloqueo
# UD4.4c - Helpers y layouts de Crispy.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


# UD4.3a - Formulario compartido por crear y actualizar.
class PerfilForm(forms.ModelForm):
    # UD4.4c - Helper sin etiqueta form y layout inicial.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('usuario'),
            Field('tipo'),
            Field('dni'),
            Field('telefono'),
            Field('fecha_alta'),
            Field('fecha_caducidad'),
        )

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
    # UD4.4c - Helper sin etiqueta form y layout inicial.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('nombre'),
            Field('tipo'),
            Field('descripcion'),
            Field('capacidad'),
            Field('activa'),
        )

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
    # UD4.4c - Helper sin etiqueta form y layout inicial.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('instalacion'),
            Field('dia_semana'),
            Field('hora_apertura'),
            Field('hora_cierre'),
            Field('duracion_franja'),
        )

    class Meta:
        model = Horario
        fields = '__all__'



# UD4.3a - Formulario compartido por crear y actualizar.
class ReservaForm(forms.ModelForm):
    # UD4.4c - Helper sin etiqueta form y layout inicial.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('usuario'),
            Field('instalacion'),
            Field('fecha'),
            Field('hora_inicio'),
            Field('hora_fin'),
            Field('estado'),
        )

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
    # UD4.4c - Helper sin etiqueta form y layout inicial.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('instalacion'),
            Field('inicio'),
            Field('fin'),
            Field('motivo'),
            Field('creado_por'),
        )

    class Meta:
        model = Bloqueo
        fields = '__all__'
