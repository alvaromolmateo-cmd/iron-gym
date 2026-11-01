from django.db import models
from django.utils import timezone


# UD3.3a - Modelo Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=256)
    apellidos = models.CharField(max_length=512)
    nif = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)


    # UD3.3b - Representación textual del cliente
    def __str__(self):
        return self.nombre + ' ' + self.apellidos + ' (' + self.nif + ')'



# UD3.3a - Modelo Factura
class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    numero = models.CharField(max_length=20)
    concepto = models.TextField()
    fecha = models.DateField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    # UD3.3b - Representación textual de la factura
    def __str__(self):
        return str(self.cliente) + ' - ' + self.numero



# UD3.3a - Modelo Cobro
class Cobro(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT)
    fecha = models.DateField(default=timezone.now)
    importe = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    # UD3.3b - Representación textual del cobro
    def __str__(self):
        return self.factura.numero + ' - ' + str(self.importe)

