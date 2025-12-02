from django.db import models

class City(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Cities'

class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    zone = models.CharField(max_length=6, help_text="Hotel zone or district")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'
