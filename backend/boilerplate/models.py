import datetime
from simple_history.models import HistoricalRecords
from simple_history import register
from djongo import models


from django.contrib.auth.models import User



class SoftDeletionQuerySet(models.QuerySet):

    """Removes soft-deleted instances from further typical querysets 
    """
    def delete(self):
        """Soft delete the following instance. It will no longer show up unless "dead" is specified"
        """
        return super(SoftDeletionQuerySet, self).update(deleted_at=datetime.datetime.now())

    def hard_delete(self):
        """True deletion of the instance, removes it from the database
        """
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        """Retrieves the non-deleted instances
        """
        return self.filter(deleted_at=None)

    def dead(self):
        """Retrieves the soft-deleted instances
        """
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.DjongoManager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class Model(models.Model):
    """Model meant to work with both the soft deletion Classes and the simple_history package
    """

    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def undelete(self):
        self.deleted_at=None
        self.save()


register(User)
