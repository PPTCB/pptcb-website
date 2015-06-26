from django.db import models


class AbstractBaseModel(models.Model):
    """
    Abstract base model is the model used for the majority of models used in the website.
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('creation time', auto_now_add=True)
    updated_at = models.DateTimeField('update time', auto_now=True)

    def __init__(self, *args, **kwargs):
        """
        Constructor override adds property cache to model instance.
        """
        super(AbstractBaseModel, self).__init__(*args, **kwargs)
        self._property_cache = dict()

    def save(self, *args, **kwargs):
        """
        Save override resets property cache on model instance.
        """
        super(AbstractBaseModel, self).save(*args, **kwargs)
        self._property_cache = dict()

    def _get_property(self, name, setter):
        """
        Retrieves cached property.
        """
        try:
            return self._property_cache[name]
        except KeyError:
            self._property_cache[name] = setter()
            return self._property_cache[name]

    class Meta:
        abstract = True