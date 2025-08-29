from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import pgettext_lazy
import datetime

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Massage(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Meta Title (50->70)"))
    meta_description = models.CharField(max_length=255, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Meta Description (90->160)"))
    meta_Keywords = models.CharField(max_length=255, null=True, help_text=pgettext_lazy("Model object", "SEO Meta Keyword (max 10)"))
    priority = models.PositiveIntegerField(default=1,help_text=pgettext_lazy("Model object", "Order index when listing, 1 is first, X last"))
    tile_label = models.CharField(max_length=100, blank=True, null=True, help_text=pgettext_lazy("Model object", "Label displayed on the tile for list view."))
    cover = models.ImageField(upload_to='img/', blank=True, null=True, help_text=pgettext_lazy("Model object", "The cover image used in tiles when listed."))
    tile_thumbnail = ImageSpecField(source='cover',
                                      processors=[ResizeToFill(353, 326)],
                                      format='JPEG',
                                      options={'quality': 60})
    calendlyURL = models.CharField(default="https://calendly.com/reservation-mi-time", blank=True, help_text=pgettext_lazy("Model object", "Full URL to calendly appointment event"))
    highlighted = models.BooleanField(default=False, help_text=pgettext_lazy("Model Object", "Different tile background color when listed"))
    price = models.DecimalField(max_digits=7, decimal_places=2, help_text=pgettext_lazy("Model object", "Price of the massage"))
    duration = models.DurationField(help_text=pgettext_lazy("Model object", "Duration of the Massage (HH:MM:SS)"), default=datetime.time(1))
    text1 = CKEditor5Field('Text', config_name='extends')
    img1 = models.ImageField(upload_to='img/', blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the massage"))
    img1_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model object", "SEO Img Alt"))
    img1_resized = ImageSpecField(source='img1',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img2 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the massage"))
    img2_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model object", "SEO Img Alt"))
    img2_resized = ImageSpecField(source='img2',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img3 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the massage"))
    img3_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model object", "SEO Img Alt"))
    img3_resized = ImageSpecField(source='img3',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})

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
    place_id = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model object", "Place id encoded by google map for this address"))

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
    meta_title = models.CharField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Meta Title (50->70)"))
    meta_description = models.CharField(max_length=255, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Meta Description (90->160)"))
    meta_Keywords = models.CharField(max_length=255, null=True, help_text=pgettext_lazy("Model object", "SEO Meta Keyword (max 10)"))
    text1 = CKEditor5Field('Text', config_name='extends')
    text2 = CKEditor5Field('Text', config_name='extends',blank=True)
    text3 = CKEditor5Field('Text', config_name='extends',blank=True)
    googlesite_url = models.URLField(blank=True, help_text=pgettext_lazy("Model object", "Google Site url"))
    slug = models.SlugField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Url Normalization"))
    cover = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "The cover image used when listed"))
    tile_thumbnail = ImageSpecField(source='cover',
                                      processors=[ResizeToFill(353, 326)],
                                      format='JPEG',
                                      options={'quality': 60})
    img1 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img1_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model object", "SEO Img Alt"))
    img1_diapo = ImageSpecField(source='img1',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img2 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img2_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model object", "SEO Img Alt"))
    img2_diapo = ImageSpecField(source='img2',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img3 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img3_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model object", "SEO Img Alt"))
    img3_diapo = ImageSpecField(source='img3',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img4 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img4_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model object", "SEO Img Alt"))
    img4_diapo = ImageSpecField(source='img4',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img5 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An image to illustrate the practice"))
    img5_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model object", "SEO Img Alt"))
    img5_diapo = ImageSpecField(source='img5',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})

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
    
    def get_diapos(self):
        diapos = {}
        for i in range (1,6):
            a_id = 'img' + str(i)
            if getattr(self, a_id) and getattr(self, a_id+'_diapo'):
                diapos[a_id] = {'alt': getattr(self, a_id+'_alt'), 'diapo': getattr(self, a_id+'_diapo').url}
        
        print(diapos)
        return diapos
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class Page(models.Model):
    class Meta:
        verbose_name = pgettext_lazy("Model object", "Page")
        verbose_name_plural = pgettext_lazy("Model object", "Pages")
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Meta Title (50->70)"))
    meta_description = models.CharField(max_length=255, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Meta Description (90->160)"))
    meta_keywords = models.CharField(max_length=255, null=True, help_text=pgettext_lazy("Model object", "SEO Meta Keyword (max 10)"))
    content = CKEditor5Field('Text', config_name='extends', blank=True, help_text=pgettext_lazy("Model object", "Content of the page"))
    custom_viewname = models.CharField(max_length=100, null=True, blank=True, help_text=pgettext_lazy("Model object", "Link custom view to its meta datas"))
    menu_position = models.SmallIntegerField(null=True, blank=True, help_text=pgettext_lazy("Model object", "Position of the item in the menu (empties won't be displayed)"))
    slug = models.SlugField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model object", "SEO Url Normalization"))

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("page", kwargs={"page_slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class SiteConfig(models.Model):
    class Meta:
        verbose_name = pgettext_lazy("Model object", "Global Site Config")
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    site_email = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model object", "Email for contacts forms"))
    header_mobile = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model object", "Mobile number in header"))
    header_openings = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model object", "Oopening time text in header"))
    facebook = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model object", "Facebook Account"))
    instagram = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model object", "Instagram Account"))
    copyright = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model object", "Copyright content in the footer"))
    design = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model object", "Design credit content in the footer"))
    placeholder_img = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model object", "An Image displayed when the original is not found"))
    robots_content = models.TextField(blank=True, help_text=pgettext_lazy("Model object", "Content of robots.txt"))
    
    def __str__(self):
        return str(self.name)