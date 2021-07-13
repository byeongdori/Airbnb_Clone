from django.db import models
from django.db.models.deletion import CASCADE
from core import models as core_models

# Create your models here.
class Conversation(core_models.AbstractTimeStampedModel):

    """Conversation Model Definition"""

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        return str(self.created)


class Message(core_models.AbstractTimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", on_delete=CASCADE)

    def __str__(self):
        return f"{self.user} says : {self.message}"
