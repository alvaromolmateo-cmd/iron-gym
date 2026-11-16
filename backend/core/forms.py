# UD4.4c - Helper y layout del formulario, como en el apartado 6.1.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms
from .models import Perfil, Instalacion, Horario, Reserva, Bloqueo


# UD4.3a - Formulario compartido por las vistas de creación y actualización.
class PerfilForm(forms.ModelForm):
    # UD4.4c / UD4.4e - Filas y columnas acordadas en el Anexo I, Tabla 2.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('usuario'), css_class='col-6'),
                Div(Field('tipo'), css_class='col-6'),
                css_class='row',
            ),
            Div(
                Div(Field('dni'), css_class='col-6'),
                Div(Field('telefono'), css_class='col-6'),
                css_class='row',
            ),
            Div(
                Div(Field('fecha_alta'), css_class='col-6'),
                Div(Field('fecha_caducidad'), css_class='col-6'),
                css_class='row',
            ),
        )

    class Meta:
        model = Perfil
        fields = '__all__'

    # UD4.3c - La caducidad es opcional, pero no puede preceder al alta.
    def clean(self):
        cleaned_data = super().clean()
        alta = cleaned_data.get('fecha_alta')
        caducidad = cleaned_data.get('fecha_caducidad')
        if alta and caducidad and caducidad < alta:
            raise forms.ValidationError('La fecha de caducidad no puede ser anterior a la fecha de alta.')
        return cleaned_data


# UD4.3a - Formulario de instalaciones.
class InstalacionForm(forms.ModelForm):
    # UD4.4c / UD4.4e - Filas y columnas acordadas en el Anexo I, Tabla 2.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('nombre'), css_class='col-8'),
                Div(Field('tipo'), css_class='col-4'),
                css_class='row',
            ),
            Div(
                Div(Field('descripcion'), css_class='col-12'),
                css_class='row',
            ),
            Div(
                Div(Field('capacidad'), css_class='col-6'),
                Div(Field('activa'), css_class='col-6'),
                css_class='row',
            ),
        )

    class Meta:
        model = Instalacion
        fields = '__all__'

    # UD4.3c - Una instalación debe admitir al menos una persona.
    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad <= 0:
            raise forms.ValidationError('La capacidad debe ser mayor que cero.')
        return capacidad


# UD4.3a - Formulario de horarios.
class HorarioForm(forms.ModelForm):
    # UD4.4c / UD4.4e - Filas y columnas acordadas en el Anexo I, Tabla 2.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('instalacion'), css_class='col-8'),
                Div(Field('dia_semana'), css_class='col-4'),
                css_class='row',
            ),
            Div(
                Div(Field('hora_apertura'), css_class='col-4'),
                Div(Field('hora_cierre'), css_class='col-4'),
                Div(Field('duracion_franja'), css_class='col-4'),
                css_class='row',
            ),
        )

    class Meta:
        model = Horario
        fields = '__all__'


# UD4.3a - fecha_creacion es automática y Django no la incluye como editable.
class ReservaForm(forms.ModelForm):
    # UD4.4c / UD4.4e - Filas y columnas acordadas en el Anexo I, Tabla 2.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('usuario'), css_class='col-6'),
                Div(Field('instalacion'), css_class='col-6'),
                css_class='row',
            ),
            Div(
                Div(Field('fecha'), css_class='col-4'),
                Div(Field('hora_inicio'), css_class='col-4'),
                Div(Field('hora_fin'), css_class='col-4'),
                css_class='row',
            ),
            Div(
                Div(Field('estado'), css_class='col-12'),
                css_class='row',
            ),
        )

    class Meta:
        model = Reserva
        fields = '__all__'

    # UD4.3c - Comprobar el intervalo antes de guardar la reserva.
    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('hora_inicio')
        fin = cleaned_data.get('hora_fin')
        if inicio and fin and fin <= inicio:
            raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')
        return cleaned_data


# UD4.3a - Formulario de bloqueos.
class BloqueoForm(forms.ModelForm):
    # UD4.4c / UD4.4e - Filas y columnas acordadas en el Anexo I, Tabla 2.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('instalacion'), css_class='col-12'),
                css_class='row',
            ),
            Div(
                Div(Field('inicio'), css_class='col-6'),
                Div(Field('fin'), css_class='col-6'),
                css_class='row',
            ),
            Div(
                Div(Field('motivo'), css_class='col-12'),
                css_class='row',
            ),
            Div(
                Div(Field('creado_por'), css_class='col-12'),
                css_class='row',
            ),
        )

    class Meta:
        model = Bloqueo
        fields = '__all__'
