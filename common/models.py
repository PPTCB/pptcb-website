from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class AbstractBaseModel(models.Model):
    """
    Abstract base model is the model used for the majority of models used in the website.
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('creation time', auto_now_add=True)
    updated_at = models.DateTimeField('update time', auto_now=True)

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
        Save override handles pre/post save events.
        """
        is_new = False if self.pk else True
        self.pre_save(is_new)
        super(AbstractBaseModel, self).save(*args, **kwargs)
        self.post_save(is_new)

    def delete(self, *args, **kwargs):
        """
        Delete override handles pre delete events
        """
        self.pre_delete()
        super(AbstractBaseModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class AbstractMPTTBaseModel(MPTTModel, AbstractBaseModel):
    """
    Abstract MPTT Base Model is the base model to use for MPTT models.
    """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        abstract = True