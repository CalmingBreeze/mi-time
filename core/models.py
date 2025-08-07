from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import pgettext_lazy
import datetime

class Siteconfig(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

class Massage(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    priority = models.PositiveIntegerField(default=1,help_text=pgettext_lazy("Model object", "Order index when listing, 1 is first, X last"))
    tcover = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "The cover image used in tiles when listed. 353*326"))
    calendlyURL = models.CharField(default="https://calendly.com/reservation-mi-time", blank=True, help_text=pgettext_lazy("Model object", "Full URL to calendly appointment event"))
    highlighted = models.BooleanField(default=False, help_text=pgettext_lazy("Model Object", "Different tile background color when listed"))
    price = models.DecimalField(max_digits=7, decimal_places=2, help_text=pgettext_lazy("Model object", "Price of the massage"))
    duration = models.DurationField(help_text=pgettext_lazy("Model object", "Duration of the Massage (HH:MM:SS)"), default=datetime.time(1))
    text1 = models.TextField()
    text2 = models.TextField(blank=True)
    text3 = models.TextField(blank=True)
    img1 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the massage"))
    img2 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the massage"))
    img3 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the massage"))

    slug = models.SlugField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO URL Normalization"))

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
        verbose_name = pgettext_lazy("Model object", "address")
        verbose_name_plural = pgettext_lazy("Model object", "addresses")

    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, help_text=pgettext_lazy("Model object", "Postal code"))
    city = models.CharField(max_length=255, help_text=pgettext_lazy("Model object", "City"))
    country = models.CharField(max_length=255, help_text=pgettext_lazy("Model object", "Country"))

    def getFormatedAddress(self):
        address = self.address1
        if self.address2:
            address += ', '+self.address2
        if self.address3:
            address += ', '+self.address3
        return address+', '+self.postal_code+' '+self.city+', '+self.country.upper()

    def __str__(self):
        return str(self.name)
    
class Openings(models.Model):
    class Meta:
        verbose_name = pgettext_lazy("Model object class", "opening")
        verbose_name_plural = pgettext_lazy("Model object class", "openings")
    
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    monday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    monday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    monday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    monday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    tuesday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    tuesday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    tuesday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    tuesday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    wednesday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    wednesday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    wednesday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    wednesday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    thursday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    thursday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    thursday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    thursday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    friday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    friday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    friday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    friday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    saturday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    saturday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    saturday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    saturday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    sunday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    sunday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    sunday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    sunday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model object", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    def getTimeTable(self):
        return {
            pgettext_lazy("Model object", 'monday'): [self.monday_open,self.monday_pause_start,self.monday_pause_end,self.monday_close],
            pgettext_lazy("Model object", 'tuesday'): [self.tuesday_open,self.tuesday_pause_start,self.tuesday_pause_end,self.tuesday_close],
            pgettext_lazy("Model object", 'wednesday'): [self.wednesday_open,self.wednesday_pause_start,self.wednesday_pause_end,self.wednesday_close],
            pgettext_lazy("Model object", 'thursday'): [self.thursday_open,self.thursday_pause_start,self.thursday_pause_end,self.thursday_close],
            pgettext_lazy("Model object", 'friday'): [self.friday_open,self.friday_pause_start,self.friday_pause_end,self.friday_close],
            pgettext_lazy("Model object", 'saturday'): [self.saturday_open,self.saturday_pause_start,self.saturday_pause_end,self.saturday_close],
            pgettext_lazy("Model object", 'sunday'): [self.sunday_open,self.sunday_pause_start,self.sunday_pause_end,self.sunday_close]
        }

    def __str__(self):
        return str(self.name)
    
class Practice(models.Model):
    class Meta:
        verbose_name = pgettext_lazy("Model object", "practice")
        verbose_name_plural = pgettext_lazy("Model object", "practices")
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    text1 = models.TextField()
    text2 = models.TextField(blank=True)
    text3 = models.TextField(blank=True)
    googlesite_url = models.URLField(blank=True, help_text=pgettext_lazy("Model object", "Google Site url"))
    slug = models.SlugField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Url Normalization"))
    cover = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "The cover image used when listed"))
    img1 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img2 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img3 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img4 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img5 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))

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

