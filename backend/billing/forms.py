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

    # UD4.3b - Validacion del formulario.
    def clean_total(self):
        total = self.cleaned_data['total']
        if total <= 0:
            raise forms.ValidationError('El total debe ser mayor que cero.')
        return total



# UD4.3a - Formulario compartido por crear y actualizar.
class CobroForm(forms.ModelForm):
    class Meta:
        model = Cobro
        fields = '__all__'

    # UD4.3b - Validacion del formulario.
    def clean_importe(self):
        importe = self.cleaned_data['importe']
        if importe <= 0:
            raise forms.ValidationError('El importe debe ser mayor que cero.')
        return importe
