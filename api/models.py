
from django.db import models
from location_field.models.plain import PlainLocationField

class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    location = PlainLocationField(based_fields=['address'], zoom=7)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)

    

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    bedroom_type = models.CharField(max_length=10, choices=[('1BHK', '1BHK'), ('2BHK', '2BHK'), ('3BHK', '3BHK'), ('4BHK', '4BHK')])
    image = models.ImageField(upload_to='unit_images/', blank=True, null=True)

    

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    document_proofs = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tenants')
    agreement_end_date = models.DateField()
    monthly_rent_date = models.PositiveIntegerField()
    
