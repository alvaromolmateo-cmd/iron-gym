from django import forms
from .models import Cliente, Factura, Cobro
# UD4.4c - Helpers y layouts de Crispy.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


# UD4.3a - Formulario compartido por crear y actualizar.
class ClienteForm(forms.ModelForm):
    # UD4.4c - Helper sin etiqueta form y layout inicial.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('nombre'),
            Field('apellidos'),
            Field('nif'),
            Field('email'),
        )

    class Meta:
        model = Cliente
        fields = '__all__'



# UD4.3a - Formulario compartido por crear y actualizar.
class FacturaForm(forms.ModelForm):
    # UD4.4c - Helper sin etiqueta form y layout inicial.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('cliente'),
            Field('numero'),
            Field('concepto'),
            Field('fecha'),
            Field('total'),
        )

    class Meta:
        model = Factura
        fields = '__all__'

    # UD4.3b - Validacion del formulario.
    def clean_total(self):
        total = self.cleaned_data['total']
        if total <= 0:
            raise forms.ValidationError('El total debe ser mayor que cero.')
        return total



# UD4.3a - Formulario compartido por crear y actualizar.
class CobroForm(forms.ModelForm):
    # UD4.4c - Helper sin etiqueta form y layout inicial.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('factura'),
            Field('fecha'),
            Field('importe'),
        )

    class Meta:
        model = Cobro
        fields = '__all__'

    # UD4.3b - Validacion del formulario.
    def clean_importe(self):
        importe = self.cleaned_data['importe']
        if importe <= 0:
            raise forms.ValidationError('El importe debe ser mayor que cero.')
        return importe
