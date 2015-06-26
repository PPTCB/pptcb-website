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

    def pre_save(self, is_new):
        """
        Code that is executed before the save method.
        """
        pass

    def post_save(self, is_new):
        """
        Code that is executed after the save method.
        """
        pass

    def pre_delete(self):
        """
        Code that is executed before the delete method.
        """
        pass

    def save(self, *args, **kwargs):
        """
        Save override resets property cache on model instance.
        Also handles pre/post save events
        """
        is_new = False if self.pk else True
        self.pre_save(is_new)
        super(AbstractBaseModel, self).save(*args, **kwargs)
        self._property_cache = dict()
        self.post_save(is_new)

    def delete(self, *args, **kwargs):
        """
        Delete override handles pre delete events
        """
        self.pre_delete()
        super(AbstractBaseModel, self).delete(*args, **kwargs)

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