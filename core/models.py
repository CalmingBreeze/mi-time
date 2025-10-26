from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import pgettext_lazy, npgettext_lazy
import datetime

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class AbstractProduct(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model Field", "SEO URL Normalization"))
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model Field", "SEO Meta Title (50->70)"))
    meta_description = models.CharField(max_length=255, null=False, unique=True, help_text=pgettext_lazy("Model Field", "SEO Meta Description (90->160)"))
    meta_Keywords = models.CharField(max_length=255, null=True, help_text=pgettext_lazy("Model Field", "SEO Meta Keyword (max 10)"))

    stripe_product_id = models.CharField(max_length=100, blank=True, null=True, help_text=pgettext_lazy("Model Field", "Stripe Product id of the product"))
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True, help_text=pgettext_lazy("Model Field", "Stripe Price id of the product"))
    price = models.DecimalField(max_digits=7, decimal_places=2, help_text=pgettext_lazy("Model Field", "Price of the product"))

    tile_label = models.CharField(max_length=100, blank=True, null=True, help_text=pgettext_lazy("Model Field", "Label displayed on the tile for list view."))
    cover = models.ImageField(upload_to='img/', blank=True, null=True, help_text=pgettext_lazy("Model Field", "The cover image used in tiles when listed."))
    tile_thumbnail = ImageSpecField(source='cover',
                                      processors=[ResizeToFill(353, 326)],
                                      format='JPEG',
                                      options={'quality': 90})
    priority = models.PositiveIntegerField(default=1,help_text=pgettext_lazy("Model Field", "Order index when listing, 1 is first, X last"))
    highlighted = models.BooleanField(default=False, help_text=pgettext_lazy("Model Field", "Different tile background color when listed"))
    text1 = CKEditor5Field('Text', config_name='extends')
    img1 = models.ImageField(upload_to='img/', blank=True, null=True, help_text=pgettext_lazy("Model Field", "An image to illustrate the massage"))
    img1_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Img Alt"))
    img1_resized = ImageSpecField(source='img1',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img2 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model Field", "An image to illustrate the massage"))
    img2_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Img Alt"))
    img2_resized = ImageSpecField(source='img2',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img3 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model Field", "An image to illustrate the massage"))
    img3_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Img Alt"))
    img3_resized = ImageSpecField(source='img3',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    
    def __str__(self):
        return str(self.name)
    
    def get_display_price(self):
        if self.price % 1 == 0:
            price = "{0:.0f}".format(self.price)
        else:
            price = "{0:.2f}".format(self.price)
        return price
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Massage(AbstractProduct):
    class Meta:
        verbose_name = npgettext_lazy("Model Class Name", "Massage", "Massages", 1)
        verbose_name_plural = npgettext_lazy("Model Class Name", "Massage", "Massages", 2)

    calendlyURL = models.CharField(default="https://calendly.com/reservation-mi-time", blank=True, help_text=pgettext_lazy("Model Field", "Full URL to calendly appointment event"))
    duration = models.DurationField(help_text=pgettext_lazy("Model Field", "Duration of the Massage (HH:MM:SS)"), default=datetime.timedelta(hours=1))

    def get_absolute_url(self):
        return reverse("massage", kwargs={"massage_slug": self.slug})
    
class GiftCard(AbstractProduct):
    class Meta:
        verbose_name = npgettext_lazy("Model Class Name", "Gift card", "Gift Cards", 1)
        verbose_name_plural = npgettext_lazy("Model Class Name", "Gift card", "Gift Cards", 2)
    
    gift_label =  models.CharField(max_length=100, null=False, help_text=pgettext_lazy("Model Field", "Gift label on the giftcard"))
    duration = models.DurationField(help_text=pgettext_lazy("Model Field", "Duration of the gifted Massage (HH:MM:SS)"), default=datetime.timedelta(hours=1))
    stripe_coupon_id = models.CharField(max_length=100, blank=True, null=True, help_text=pgettext_lazy("Model Field", "Stripe Coupon id of the gift card"))
    
    def get_absolute_url(self):
        return reverse("giftcard", kwargs={"giftcard_slug": self.slug})
    
class Bundle(AbstractProduct):
    class Meta:
        verbose_name = npgettext_lazy("Model Class Name", "Bundle", "Bundles", 1)
        verbose_name_plural = npgettext_lazy("Model Class Name", "Bundle", "Bundles", 2)
    
    duration = models.DurationField(help_text=pgettext_lazy("Model Field", "Total massage credit duration of the bundle"), default=datetime.timedelta(hours=3))
    
    def get_absolute_url(self):
        return reverse("bundle", kwargs={"bundle_slug": self.slug})

class Address(models.Model):
    class Meta:
        verbose_name = npgettext_lazy("Model Class Name", "Address", "Addresses", 1)
        verbose_name_plural = npgettext_lazy("Model Class Name", "Address", "Addresses", 2)

    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, help_text=pgettext_lazy("Model Field", "Postal code"))
    city = models.CharField(max_length=255, help_text=pgettext_lazy("Model Field", "City"))
    country = models.CharField(max_length=255, help_text=pgettext_lazy("Model Field", "Country"))
    place_id = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model Field", "Place id encoded by google map for this address"))

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
        verbose_name = npgettext_lazy("Model Class Name", "Opening", "Openings", 1)
        verbose_name_plural = npgettext_lazy("Model Class Name", "Opening", "Openings", 2)
    
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    monday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    monday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    monday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    monday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    tuesday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    tuesday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    tuesday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    tuesday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    wednesday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    wednesday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    wednesday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    wednesday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    thursday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    thursday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    thursday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    thursday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    friday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    friday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    friday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    friday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    saturday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    saturday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    saturday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    saturday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    sunday_open = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Opening")+" (HH:MM:SS)", default=datetime.time(10, 00))
    sunday_pause_start = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Lunchbreak")+" (HH:MM:SS)", default=datetime.time(13, 00))
    sunday_pause_end = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "End of the Lunchbreak")+" (HH:MM:SS)", default=datetime.time(15, 00))
    sunday_close = models.TimeField(blank=True, null=True, help_text=pgettext_lazy("Model Field", "Closing")+" (HH:MM:SS)", default=datetime.time(18, 00))

    def getTimeTable(self):
        return {
            pgettext_lazy("Model Field", 'monday'): [self.monday_open,self.monday_pause_start,self.monday_pause_end,self.monday_close],
            pgettext_lazy("Model Field", 'tuesday'): [self.tuesday_open,self.tuesday_pause_start,self.tuesday_pause_end,self.tuesday_close],
            pgettext_lazy("Model Field", 'wednesday'): [self.wednesday_open,self.wednesday_pause_start,self.wednesday_pause_end,self.wednesday_close],
            pgettext_lazy("Model Field", 'thursday'): [self.thursday_open,self.thursday_pause_start,self.thursday_pause_end,self.thursday_close],
            pgettext_lazy("Model Field", 'friday'): [self.friday_open,self.friday_pause_start,self.friday_pause_end,self.friday_close],
            pgettext_lazy("Model Field", 'saturday'): [self.saturday_open,self.saturday_pause_start,self.saturday_pause_end,self.saturday_close],
            pgettext_lazy("Model Field", 'sunday'): [self.sunday_open,self.sunday_pause_start,self.sunday_pause_end,self.sunday_close]
        }

    def __str__(self):
        return str(self.name)
    
class Practice(models.Model):
    class Meta:
        verbose_name = npgettext_lazy("Model Class Name", "Practice", "Practices", 1)
        verbose_name_plural = npgettext_lazy("Model Class Name", "Practice", "Practices", 2)
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model Field", "SEO Meta Title (50->70)"))
    meta_description = models.CharField(max_length=255, null=False, unique=True, help_text=pgettext_lazy("Model Field", "SEO Meta Description (90->160)"))
    meta_Keywords = models.CharField(max_length=255, null=True, help_text=pgettext_lazy("Model Field", "SEO Meta Keyword (max 10)"))
    text1 = CKEditor5Field('Text', config_name='extends')
    text2 = CKEditor5Field('Text', config_name='extends', blank=True, help_text=pgettext_lazy("Model Field", "Additionnal content of the page"))
    text3 = CKEditor5Field('Text', config_name='extends', blank=True, help_text=pgettext_lazy("Model Field", "Additionnal content of the page"))
    googlesite_url = models.URLField(blank=True, help_text=pgettext_lazy("Model Field", "Google Site url"))
    slug = models.SlugField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model Field", "SEO Url Normalization"))
    cover = models.ImageField(upload_to='img/', blank=True, null=True, help_text=pgettext_lazy("Model Field", "The cover image used when listed"))
    tile_thumbnail = ImageSpecField(source='cover',
                                      processors=[ResizeToFill(353, 326)],
                                      format='JPEG',
                                      options={'quality': 60})
    img1 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model Field", "An image to illustrate the practice"))
    img1_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Img Alt"))
    img1_diapo = ImageSpecField(source='img1',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img2 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model Field", "An image to illustrate the practice"))
    img2_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Img Alt"))
    img2_diapo = ImageSpecField(source='img2',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img3 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model Field", "An image to illustrate the practice"))
    img3_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Img Alt"))
    img3_diapo = ImageSpecField(source='img3',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img4 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model Field", "An image to illustrate the practice"))
    img4_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Img Alt"))
    img4_diapo = ImageSpecField(source='img4',
                                      processors=[ResizeToFill(400, 250)],
                                      format='JPEG',
                                      options={'quality': 60})
    img5 = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model Field", "An image to illustrate the practice"))
    img5_alt = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Img Alt"))
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
        
        return diapos
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class Page(models.Model):
    class Meta:
        verbose_name = npgettext_lazy("Model Class Name", "Page", "Pages", 1)
        verbose_name_plural = npgettext_lazy("Model Class Name", "Page", "Pages", 2)
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=100, null=False, unique=True, help_text=pgettext_lazy("Model Field", "SEO Meta Title (50->70)"))
    meta_description = models.CharField(max_length=255, null=False, unique=True, help_text=pgettext_lazy("Model Field", "SEO Meta Description (90->160)"))
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Meta Keyword (max 10)"))
    meta_robots = models.CharField(max_length=255, blank=True, null=True, help_text=pgettext_lazy("Model Field", "SEO Meta Robots"))
    text = CKEditor5Field('Text', config_name='extends', blank=True, help_text=pgettext_lazy("Model Field", "Content of the page"))
    text2 = CKEditor5Field('Text', config_name='extends', blank=True, help_text=pgettext_lazy("Model Field", "Additionnal content of the page"))
    text3 = CKEditor5Field('Text', config_name='extends', blank=True, help_text=pgettext_lazy("Model Field", "Additionnal content of the page"))
    custom_viewname = models.CharField(max_length=100, null=True, blank=True, help_text=pgettext_lazy("Model Field", "Link custom view to its meta datas"))
    legal_page = models.BooleanField(default=False, help_text=pgettext_lazy("Model Field", "Page legaly required ? (displayed under the footer)"))
    menu_position = models.SmallIntegerField(null=True, blank=True, help_text=pgettext_lazy("Model Field", "Position of the item in the menu (empties won't be displayed)"))
    footer_position = models.SmallIntegerField(null=True, blank=True, help_text=pgettext_lazy("Model Field", "Position of the item in footer links section (empties won't be displayed)"))
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True, help_text=pgettext_lazy("Model Field", "SEO Url Normalization"))

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
        verbose_name = npgettext_lazy("Model Class Name", "Global Site Config", "Global Site Configs", 1)
        verbose_name_plural = npgettext_lazy("Model Class Name", "Global Site Config", "Global Site Configs", 2)
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    site_email = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model Field", "Email visible on the website"))
    header_mobile = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model Field", "Main Mobile number visible on the website"))
    header_openings = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model Field", "Opening time text in header"))
    footer_about_title = models.CharField(max_length=100, default="Mireille", blank=True, help_text=pgettext_lazy("Model Field", "Title of the about block in footer"))
    footer_about_text = CKEditor5Field('Text', config_name='extends', blank=True, help_text=pgettext_lazy("Model Field", "Content of the about block in footer"))
    facebook = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model Field", "Facebook Account"))
    instagram = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model Field", "Instagram Account"))
    copyright = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model Field", "Copyright content in the footer"))
    design = models.CharField(max_length=255, blank=True, help_text=pgettext_lazy("Model Field", "Design credit content in the footer"))
    placeholder_img = models.ImageField(upload_to='img/',blank=True, null=True, help_text=pgettext_lazy("Model Field", "An Image displayed when the original is not found"))
    robots_content = models.TextField(blank=True, help_text=pgettext_lazy("Model Field", "Content of robots.txt"))
    
    def __str__(self):
        return str(self.name)