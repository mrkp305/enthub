from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    
    name = models.CharField("Country or Area Name", max_length=50)
    iso_code2 = models.CharField("ISO ALPHA-2 Code", max_length=2, unique=True)
    iso_code3 = models.CharField("ISO ALPHA-3 Code", primary_key=True, max_length=3)
    iso_num = models.PositiveSmallIntegerField("ISO Numeric Code UN M49 Numerical Code", unique=True, validators=[MaxValueValidator(999)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

class City(models.Model):
    name = models.CharField("City name", max_length=50)
    country = models.ForeignKey(Country, verbose_name="Country Code", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return "{} - {}".format(self.name, self.country)

class Tag(models.Model):
    name = models.CharField("Tag name", max_length=30)


    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(_("Genre"), max_length=50, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name

class EventType(models.Model):
    name = models.CharField(_("Event Type"), max_length=50)

    class Meta:
        verbose_name = 'Event type'
        verbose_name_plural = 'Event types'

    def __str__(self):
            return self.name
    
class EventPurpose(models.Model):
    purpose = models.CharField(_("Purpose"), max_length=50)

    class Meta:
    
        verbose_name = 'Purpose'
        verbose_name_plural = 'Venue Purposes'

    def __str__(self):
        return self.purpose
    
    