from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
import datetime

# Create your models here.
class Massage(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, help_text="Price of the massage")
    duration = models.DurationField(help_text="Duration of the Massage (in HH:MM:SS format)", default=datetime.time(1))
    text1 = models.TextField()
    text2 = models.TextField(blank=True)
    text3 = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, null=False, unique=True, help_text="SEO Url Normalization")

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("massage", kwargs={"massage_slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Address(models.Model):
    class Meta:
        verbose_name_plural = "addresses"

    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, help_text="Postal code of the address")
    city = models.CharField(max_length=255, help_text="City of the address")
    country = models.CharField(max_length=255, help_text="Country of the address")
    
    def __str__(self):
        return str(self.name)
    
class Openings(models.Model):
    class Meta:
        verbose_name_plural = "openings"
    
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    monday_open = models.TimeField(blank=True, null=True, help_text="Monday opening hour, HH:MM:SS", default=datetime.time(10, 00))
    monday_pause_start = models.TimeField(blank=True, null=True, help_text="Monday start of the Lunchbreak, HH:MM:SS", default=datetime.time(13, 00))
    monday_pause_end = models.TimeField(blank=True, null=True, help_text="Monday end of the Lunchbreak, HH:MM:SS", default=datetime.time(15, 00))
    monday_close = models.TimeField(blank=True, null=True, help_text="Monday closing hour, HH:MM:SS", default=datetime.time(18, 00))

    tuesday_open = models.TimeField(blank=True, null=True, help_text="Tuesday opening hour, HH:MM:SS", default=datetime.time(10, 00))
    tuesday_pause_start = models.TimeField(blank=True, null=True, help_text="Tuesday start of the Lunchbreak, HH:MM:SS", default=datetime.time(13, 00))
    tuesday_pause_end = models.TimeField(blank=True, null=True, help_text="Tuesday end of the Lunchbreak, HH:MM:SS", default=datetime.time(15, 00))
    tuesday_close = models.TimeField(blank=True, null=True, help_text="Tuesday closing hour, HH:MM:SS", default=datetime.time(18, 00))

    wednesday_open = models.TimeField(blank=True, null=True, help_text="Wednesday opening hour, HH:MM:SS", default=datetime.time(10, 00))
    wednesday_pause_start = models.TimeField(blank=True, null=True, help_text="Wednesday start of the Lunchbreak, HH:MM:SS", default=datetime.time(13, 00))
    wednesday_pause_end = models.TimeField(blank=True, null=True, help_text="Wednesday end of the Lunchbreak, HH:MM:SS", default=datetime.time(15, 00))
    wednesday_close = models.TimeField(blank=True, null=True, help_text="Wednesday closing hour, HH:MM:SS", default=datetime.time(18, 00))

    thursday_open = models.TimeField(blank=True, null=True, help_text="Thursday opening hour, HH:MM:SS", default=datetime.time(10, 00))
    thursday_pause_start = models.TimeField(blank=True, null=True, help_text="Thursday start of the Lunchbreak, HH:MM:SS", default=datetime.time(13, 00))
    thursday_pause_end = models.TimeField(blank=True, null=True, help_text="Thursday end of the Lunchbreak, HH:MM:SS", default=datetime.time(15, 00))
    thursday_close = models.TimeField(blank=True, null=True, help_text="Thursday closing hour, HH:MM:SS", default=datetime.time(18, 00))

    friday_open = models.TimeField(blank=True, null=True, help_text="Friday opening hour, HH:MM:SS", default=datetime.time(10, 00))
    friday_pause_start = models.TimeField(blank=True, null=True, help_text="Friday start of the Lunchbreak, HH:MM:SS", default=datetime.time(13, 00))
    friday_pause_end = models.TimeField(blank=True, null=True, help_text="Friday end of the Lunchbreak, HH:MM:SS", default=datetime.time(15, 00))
    friday_close = models.TimeField(blank=True, null=True, help_text="Friday closing hour, HH:MM:SS", default=datetime.time(18, 00))

    saturday_open = models.TimeField(blank=True, null=True, help_text="Saturday opening hour, HH:MM:SS", default=datetime.time(10, 00))
    saturday_pause_start = models.TimeField(blank=True, null=True, help_text="Saturday start of the Lunchbreak, HH:MM:SS", default=datetime.time(13, 00))
    saturday_pause_end = models.TimeField(blank=True, null=True, help_text="Saturday end of the Lunchbreak, HH:MM:SS", default=datetime.time(15, 00))
    saturday_close = models.TimeField(blank=True, null=True, help_text="Saturday closing hour, HH:MM:SS", default=datetime.time(18, 00))

    sunday_open = models.TimeField(blank=True, null=True, help_text="Sunday opening hour, HH:MM:SS", default=datetime.time(10, 00))
    sunday_pause_start = models.TimeField(blank=True, null=True, help_text="Sunday start of the Lunchbreak, HH:MM:SS", default=datetime.time(13, 00))
    sunday_pause_end = models.TimeField(blank=True, null=True, help_text="Sunday end of the Lunchbreak, HH:MM:SS", default=datetime.time(15, 00))
    sunday_close = models.TimeField(blank=True, null=True, help_text="Sunday closing hour, HH:MM:SS", default=datetime.time(18, 00))

    def __str__(self):
        return str(self.name)
    
class Practice(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    text1 = models.TextField()
    text2 = models.TextField(blank=True)
    text3 = models.TextField(blank=True)
    googlesite_url = models.URLField(blank=True, help_text="Google Site url")
    slug = models.SlugField(max_length=100, null=False, unique=True, help_text="SEO Url Normalization")

    address = models.OneToOneField(
        Address,
        on_delete = models.CASCADE,
        null=True, 
        blank=True
    )

    opening = models.ForeignKey(
        Openings,
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )

    massages = models.ManyToManyField(Massage, blank=True)
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("practice", kwargs={"practice_slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

