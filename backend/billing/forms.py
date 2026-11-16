from django import forms
from .models import Cliente, Factura, Cobro


# UD4.3a - Formulario compartido por crear y actualizar.
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'



# UD4.3a - Formulario compartido por crear y actualizar.
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'



# UD4.3a - Formulario compartido por crear y actualizar.
class CobroForm(forms.ModelForm):
    class Meta:
        model = Cobro
        fields = '__all__'
