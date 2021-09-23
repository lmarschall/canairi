from django.db import models

class Measurement(models.Model):
    time = models.DateTimeField(default=0)
    temperature = models.FloatField(default=0.0)
    pressure = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    gas_resistance = models.FloatField(default=0.0)
    air_quality = models.IntegerField(default=0.0)

    class Meta:
        db_table = 'app_measurements'
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'