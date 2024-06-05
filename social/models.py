from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class FriendRequest(models.Model):
    class Status(models.IntegerChoices):
        SENT = 0
        ACCEPT = 1
        REJECT = 2

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.IntegerField(choices=Status.choices, default=Status.SENT)

    class Meta:
        unique_together = ('sender', 'receiver')

    def accept(self):
        self.status = self.Status.ACCEPT
        self.save(update_fields=['status'])

    def reject(self):
        self.delete()
