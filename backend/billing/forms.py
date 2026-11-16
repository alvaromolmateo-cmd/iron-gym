# UD4.4c - Helper y layout del formulario, como en el apartado 6.1.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms
from .models import Cliente, Factura, Cobro


# UD4.3a - Un ModelForm compartido por ClienteCreateView y ClienteUpdateView.
class ClienteForm(forms.ModelForm):
    # UD4.4c / UD4.4d - Distribucion de billing indicada en la Tabla 2.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('nombre'), css_class='col-3'),
                Div(Field('apellidos'), css_class='col-6'),
                Div(Field('nif'), css_class='col-3'),
                css_class='row',
            ),
            Div(
                Div(Field('email'), css_class='col-12'),
                css_class='row',
            ),
        )

    class Meta:
        model = Cliente
        fields = '__all__'


# UD4.3a - Formulario de creación y actualización de facturas.
class FacturaForm(forms.ModelForm):
    # UD4.4c / UD4.4d - Distribucion de billing indicada en la Tabla 2.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('cliente'), css_class='col-12'),
                css_class='row',
            ),
            Div(
                Div(Field('numero'), css_class='col-4'),
                Div(Field('fecha'), css_class='col-4'),
                Div(Field('total'), css_class='col-4'),
                css_class='row',
            ),
            Div(
                Div(Field('concepto'), css_class='col-12'),
                css_class='row',
            ),
        )

    class Meta:
        model = Factura
        fields = '__all__'

    # UD4.3b - El importe de la factura se llama total en nuestro modelo.
    def clean_total(self):
        total = self.cleaned_data['total']
        if total <= 0:
            raise forms.ValidationError('El total debe ser mayor que cero.')
        return total


# UD4.3a - Formulario de creación y actualización de cobros.
class CobroForm(forms.ModelForm):
    # UD4.4c / UD4.4d - Distribucion de billing indicada en la Tabla 2.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('factura'), css_class='col-12'),
                css_class='row',
            ),
            Div(
                Div(Field('fecha'), css_class='col-6'),
                Div(Field('importe'), css_class='col-6'),
                css_class='row',
            ),
        )

    class Meta:
        model = Cobro
        fields = '__all__'

    # UD4.3b - Validación del importe antes de ejecutar form_valid en la vista.
    def clean_importe(self):
        importe = self.cleaned_data['importe']
        if importe <= 0:
            raise forms.ValidationError('El importe debe ser mayor que cero.')
        return importe
