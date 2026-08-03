from django.db import models


class Info(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    email = models.EmailField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    google_place_id = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    timetable = models.TextField()
    social = models.TextField()

    class Meta:
        verbose_name = 'Información de contacto'
        verbose_name_plural = 'Información de contacto'

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}'

    @classmethod
    def get(cls):
        return cls.objects.get(pk=1)

    @property
    def google_maps_url(self):
        return f'https://www.google.com/maps/place/?q=place_id:{self.google_place_id}'

    @property
    def google_reviews_url(self):
        return f'https://search.google.com/local/writereview?placeid={self.google_place_id}'

    @property
    def google_maps_embed_url(self):
        return f'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4260.874776241323!2d{self.longitude}!3d{self.latitude}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xc6a89d10550a4fd%3A0x42d73de50c685f8!2sPizzer%C3%ADa%20La%20Albahaca!5e1!3m2!1ses!2ses!4v1779018265403!5m2!1ses!2ses'


class Vacation(models.Model):
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(verbose_name='Fecha de fin')

    def __str__(self):
        return f'Vacaciones desde {self.start_date} hasta {self.end_date}'

    class Meta:
        verbose_name = 'Vacaciones'
        verbose_name_plural = 'Vacaciones'
        ordering = ['-start_date']

    @classmethod
    def is_vacation(cls, date):
        return cls.objects.filter(start_date__lte=date, end_date__gte=date).exists()
