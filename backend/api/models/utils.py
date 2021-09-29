import datetime
from simple_history.models import HistoricalRecords
from djongo import models

class QuerySet(models.QuerySet):

    """Removes soft-deleted instances from further typical querysets 
    """
    def delete(self):
        """Soft delete the following instance. It will no longer show up unless "dead" is specified"
        """
        return super(QuerySet, self).update(deleted_at=datetime.datetime.now())

    def hard_delete(self):
        """True deletion of the instance, removes it from the database
        """
        return super(QuerySet, self).delete()

    def alive(self):
        """Retrieves the non-deleted instances
        """
        return self.filter(deleted_at=None)

    def dead(self):
        """Retrieves the soft-deleted instances
        """
        return self.exclude(deleted_at=None)


class ModelManager(models.DjongoManager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(ModelManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return QuerySet(self.model).filter(deleted_at=None)
        return QuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class Model(models.Model):
    """
    Model meant to work with both the soft deletion Classes and the simple_history package.
    Adds a numerical id, as opposed to the string-type id MongoDB uses"""

    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    objects = ModelManager()
    all_objects = ModelManager(alive_only=False)
    history = HistoricalRecords(inherit=True)

    id = models.BigAutoField(primary_key=True)
    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def undelete(self):
        self.deleted_at=None
        self.save()

