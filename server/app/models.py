from django.db import models

class Measurement(models.Model):
    time = models.DateTimeField(default=0)
    value = models.IntegerField(default=0)

    class Meta:
        db_table = 'app_measurements'
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurement'