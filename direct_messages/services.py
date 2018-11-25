from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

from .models import Message,ChatRoom
from . signals import message_read,message_sent


class MessagingService:

    def send_messages(self, sender, recipient, message):
        if sender == recipient:
            raise ValidationError("You can't send message to yourself")

        message = Message(sender=sender, recipient=recipient, content=str(message))
        message.save()

        message_sent.send(sender=message, form_user=message.sender, to=message.recipient)

        return message, 200

    def get_unread_message(self, user):
        return Message.objects.all().filter(recipient=user, read_at=None)

    def read_message(self,message_id):
        try:
            message = Message.objects.get(id=message_id)
            self.mark_as_read(message)
            return message.sender.username+':'+message.content
        except Message.DoesNotExist:
            return ''

    def mark_as_read(self, message):
        if message.read_at is None:
            message.read_at = timezone.now()
            message_read.send(sender=message, from_user=message.sender, to=message.recipient)
            message.save()

    def get_conversation(self, user):
        """
        获取当前用户的对话列表
        """
        chatrooms = ChatRoom.objects.filter(Q(sender=user) | Q(recipient=user))
        chatrooms_mapper = []
        for chatroom in chatrooms:
            chatroom_dict={}
            chatroom_dict['pk'] = chatroom.pk

            if user ==chatroom.sender:
                recipient = chatroom.recipient

            else:
                recipient = chatroom.sender

            chatroom_dict['recipient']=recipient
            chatrooms_mapper.append(chatroom_dict)

        return chatrooms_mapper

    def get_active_conversations(self, sender,recipient):

        active_conversations = Message.objects.filter(
            ((Q(sender=sender) & Q(recipient=recipient)) | (Q(sender=recipient) & Q(recipient=sender)))
        ).order_by('sent_at')

        return  active_conversations




