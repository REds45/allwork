from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
# Create your models here.

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ChatRoom(models.Model):

    sender = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chatroom_sender',
        verbose_name='Sender'
    )
    recipient = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='chatroom_recipient')

    created_at = models.DateTimeField('sent at', auto_now=True)

    class Meta:
        ordering=['-created_at']
        unique_together = ('sender', 'recipient')


class Message(models.Model):
    content = models.TextField('Contend')  # 消息文本
    sender = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='send_dm', verbose_name='Sender',
    )
    recipient = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='received_dm', verbose_name='Recipient',
    )
    sent_at = models.DateTimeField('sent at', auto_now_add=True)  # 发送时间
    read_at = models.DateTimeField('read at', null=True, blank=True)  # 读取时间

    class Meta:
        ordering = ['-sent_at']

    @property
    def unread(self):
        if self.read_at is not None:
            return True

    def __str__(self):
        return  self.content

    def save(self, **kwargs):
        if self.sender == self.recipient:
            raise ValidationError("You can't send a message to yourself")

        if not self.id:
            self.send_at = timezone.now()
        super(Message, self).save(**kwargs)


