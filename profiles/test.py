from django.test import TestCase
from .models import Relationship
from django.contrib.auth.models import User

class RelationshipTestCase(TestCase):
    def create_users(self):
        a = User.objects.create(username = 'a')
        b = User.objects.create(username = 'b')
        c = User.objects.create(username = 'c')
        d = User.objects.create(username = 'd')
        return (a,b,c,d)

    def test_relationship_status(self):
        a, b, c, d = self.create_users()
        e = User.objects.create(username = 'e')
        Relationship.objects.send_friend_request(a, b)
        Relationship.objects.send_friend_request(a,c)
        Relationship.objects.accept_friend_request(a, b)
        Relationship.objects.send_friend_request(d, a)
        self.assertEqual(Relationship.objects.relationship_status(a, b), "friend")
        self.assertEqual(Relationship.objects.relationship_status(a, c), "request_sent")
        self.assertEqual(Relationship.objects.relationship_status(a, d), "request_received")
        self.assertEqual(Relationship.objects.relationship_status(a, e), "no_relation")
        self.assertEqual(Relationship.objects.relationship_status(a, a), "same_person")



    def test_relationship_existence(self):
        a,b,c,d = self.create_users()
        Relationship.objects.send_friend_request(a, b)
        Relationship.objects.send_friend_request(a,c)
        Relationship.objects.accept_friend_request(a, b)
        self.assertEqual(Relationship.objects.relation_existence_check(a,b), True)
        self.assertEqual(Relationship.objects.relation_existence_check(a,c), True)
        self.assertEqual(Relationship.objects.relation_existence_check(a,d), False)

    def test_friend_existence(self):
        a,b,c,d = self.create_users()
        Relationship.objects.send_friend_request(a, b)
        Relationship.objects.send_friend_request(a,c)
        Relationship.objects.accept_friend_request(a, b)
        self.assertEqual(Relationship.objects.friend_existence_check(a,b), True)
        self.assertEqual(Relationship.objects.friend_existence_check(b,a), True)
        self.assertEqual(Relationship.objects.friend_existence_check(a, c), False)
        self.assertEqual(Relationship.objects.friend_existence_check(c, a), False)
        self.assertEqual(Relationship.objects.friend_existence_check(a, d), False)


    def test_send_friend_request(self):
        a, b, c, d = self.create_users()
        Relationship.objects.send_friend_request(a, b)
        Relationship.objects.send_friend_request(c, b)
        self.assertEqual(Relationship.objects.get_friend_request_list(user = b), [a, c])

    def test_sent_friend_request_list(self):
        a, b, c, d = self.create_users()
        Relationship.objects.send_friend_request(a, b)
        Relationship.objects.send_friend_request(a, c)
        self.assertEqual(Relationship.objects.get_sent_friend_request_list(user = a), [b, c])

    def test_multiple_friend_request(self):
        a, b, c, d = self.create_users()
        Relationship.objects.send_friend_request(a, b)
        self.assertFalse(Relationship.objects.send_friend_request(a, b))

    def test_accept_friend_request_without_sent(self):
        a, b, c, d = self.create_users()
        self.assertFalse(Relationship.objects.accept_friend_request(a, b))
        
        
    def test_accept_friend_request(self):
        a, b, c, d = self.create_users()
        Relationship.objects.send_friend_request(a, b)
        Relationship.objects.send_friend_request(c, b)
        Relationship.objects.send_friend_request(b, d)

        Relationship.objects.accept_friend_request(a, b)
        Relationship.objects.accept_friend_request(b, d)

        self.assertEqual(Relationship.objects.get_friend_list(user = b), [a, d])
    
