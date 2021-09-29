
from .utils import Model
from .user import User
from djongo import models


class Message(Model):

    """Relatively generic model with two owners
    """

    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='sender')
    recepient = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='recepient')

    timestamp = models.DateTimeField(auto_now=True)

    title = models.CharField(null=False, max_length=64)
    body = models.CharField(null=False, max_length=2048)

    read = models.ArrayReferenceField(to=User, related_name='has_read', null=True)
    deleted = models.ArrayReferenceField(to=User, related_name='has_deleted', null=True)

# __all__ = [ Message, User]
