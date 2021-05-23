from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    bio = models.TextField(default = '')
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username
    

RelationshipChoices = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
)
class RelationshipManager(models.Manager):
    def send_friend_request(self, sender, receiver):
        if self.relation_existence_check(sender, receiver) == False:
            Relationship.objects.create(sender = sender, receiver = receiver, status = 'pending')
            return True
        else: return False


    def accept_friend_request(self, sender, receiver):
        try:
            relationship = Relationship.objects.get(sender = sender, receiver = receiver, status = 'pending')
            relationship.status = 'accepted'
            relationship.save()
            return True
        except Relationship.DoesNotExist:
            return False

    def remove_relationship(self, user1, user2):
        try:
            relationship = Relationship.objects.get(
                models.Q(sender = user1, receiver = user2)  |
                models.Q(sender = user2, receiver = user1) )
            relationship.delete()
            return True
        except Relationship.DoesNotExist:
            return False

    def relation_existence_check(self, user1, user2):
        relationship = Relationship.objects.filter( 
            models.Q(sender = user1, receiver = user2)  |
            models.Q(sender = user2, receiver = user1)
            )
        return relationship.exists()

    def friend_existence_check(self, user1, user2):
        relationship = Relationship.objects.filter(
            (models.Q(sender = user1, receiver = user2) |
            models.Q(sender = user2, receiver = user1) ) &
            models.Q(status = "accepted") 
        )
        return relationship.exists()

    def relationship_status(self, own, another):
        if(own == another): 
            return "same_person"
        if(Relationship.objects.relation_existence_check(own, another) == False):
            return "no_relation"
        if(Relationship.objects.friend_existence_check(own, another)):
            return "friend"
        if(Relationship.objects.filter(sender = own, receiver = another, status = 'pending')):
            return "request_sent"
        if(Relationship.objects.filter(sender = another, receiver = own, status = 'pending')):
            return "request_received"

    def get_friend_request_list(self, user):
        sender_id_list = Relationship.objects.filter(receiver=user, status = 'pending').values_list('sender')
        sender_user_list = []
        for sender in sender_id_list:
            user = User.objects.get(pk = sender[0]) #because sender is a (pk, ) like tuple
            sender_user_list.append(user)
        return sender_user_list

    def get_sent_friend_request_list(self, user):
        receiver_id_list = Relationship.objects.filter(sender = user, status = 'pending').values_list('receiver')
        receiver_user_list = []
        for receiver in receiver_id_list:
            user = User.objects.get(pk = receiver[0])
            receiver_user_list.append(user)
        return receiver_user_list

    def get_friend_list(self, user):
        relationship_list = Relationship.objects.filter(
            (models.Q(receiver = user) | models.Q(sender = user)) & models.Q(status = 'accepted')
        ).values_list('sender', 'receiver')

        friend_list = []
        for relationship in relationship_list:
            if relationship[0] == user.pk: friend_pk = relationship[1]
            else: friend_pk = relationship[0]
            friend_list.append(User.objects.get(pk = friend_pk))
        return friend_list

    def get_friend_count(self, user):
        return Relationship.objects.filter(
            (models.Q(receiver = user) | models.Q(sender = user)) & models.Q(status = 'accepted')
            ).count()


class Relationship(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'sender') # sender isnt a meaningful rel name. dont u think?
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'receiver')
    status = models.CharField(max_length=8, choices=RelationshipChoices)
    objects = RelationshipManager()

    def __str__(self):
        return self.sender.username + " " + self.receiver.username
    


