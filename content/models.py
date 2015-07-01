from django.db import models
from django.utils.functional import cached_property

from core.intl import states
from core.models import AbstractBaseModel, AbstractMPTTBaseModel


class Page(AbstractMPTTBaseModel):
    HOME_PAGE_SLUG = 'home'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    override_url = models.CharField(max_length=1000, default='')

    @cached_property
    def full_name(self):
        """
        Display name with ancestors' names.
        """
        if self.parent:
            if self.parent.is_home_page:
                return self.name
            else:
                return self.parent.full_name + ' | ' + self.name
        else:
            return self.name

    @cached_property
    def is_home_page(self):
        """
        If this page is the home page of the website.
        """
        if not self.parent and self.slug.lower() == self.HOME_PAGE_SLUG:
            return True
        return False

    @cached_property
    def system_path(self):
        """
        System URL path.
        """
        if self.parent:
            path = self.parent.system_path.strip('/')
            path = path + '/' + self.slug
        elif self.is_home_page:
            return '/'
        else:
            path = self.slug
        path = path.strip('/')
        return "/%s/" % path

    def pre_save(self, is_new):
        # Need to clean the slug before database change.
        self._clean_slug()

    def _clean_slug(self):
        """
        Cleans the URL slug.
        """
        # If the slug does not exist or is blank, create one from title.
        if not self.slug or self.slug.strip() == '':
            self._generate_slug()
        # Else force the user's input to a properly formatted slug.
        else:
            self.slug = self.url_friendly_string(self.slug)

    def _generate_slug(self):
        """
        Makes a URL slug out of the title.
        """
        self.slug = self.url_friendly_string(self.title)

    @staticmethod
    def url_friendly_string(input_string):
        """
        Converts a string into a format that is URL friendly.
        """
        output = input_string.lower().strip().replace(' ', '-')
        # TODO: replace invalid characters
        return output

    class Meta:
        unique_together = (('title', 'parent'), ('slug', 'parent'))


class Address(AbstractBaseModel):
    STATE_CHOICES = (
        ('US', states.us_states_abbr),
        ('US Territories', states.us_territories_abbr),
        ('Canada', states.canada_provinces_abbr),
    )

    street_line_1 = models.CharField(max_length=255)
    street_line_2 = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    postal_code = models.CharField(max_length=15)

    def __unicode__(self):
        if self.street_line_2:
            return "%s, %s, %s, %s %s" % (self.street_line_1, self.street_line_2, self.city, self.state, self.postal_code)
        else:
            return "%s, %s, %s %s" % (self.street_line_1, self.city, self.state, self.postal_code)

    class Meta:
        unique_together = ('street_line_1', 'street_line_2', 'city', 'state')
        verbose_name_plural = 'addresses'


class Location(AbstractBaseModel):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address)
    phone_number_1 = models.CharField('primary phone number', max_length=30, default='', blank=True)
    phone_number_2 = models.CharField('secondary phone number', max_length=30, default='', blank=True)
    fax_number = models.CharField(max_length=30, default='', blank=True)
    email = models.EmailField(null=True, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.address)

    class Meta:
        unique_together = ('name', 'address')


class Event(AbstractBaseModel):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name