from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Relationship
from radio.models import Post

# Create your tests here.

class PostsTestCase(TestCase):
    def create_friends(self):
        a = User(username = 'a')
        a.save()
        b = User(username = 'b')
        b.save()
        c = User(username = 'c') 
        c.save()
        d = User(username = 'd')
        d.save()
        Relationship.objects.send_friend_request(a, b)
        Relationship.objects.send_friend_request(a, c)
        Relationship.objects.send_friend_request(a, d)
        Relationship.objects.accept_friend_request(a, b)
        Relationship.objects.accept_friend_request(a, c)
        Relationship.objects.accept_friend_request(a, d)

        return (a, b, c, d)

    def create_post(self, author):
        for i in range(8):
            Post.objects.create(author = author, yt_code = (author.username + str(i)))

    def test_get_all_friends_post(self):
        a, b, c, d = self.create_friends()
        for author in [a, b, c, d]:
            self.create_post(author)
        posts = Post.objects.get_friends_and_own_posts(a)
        self.assertEqual(len(posts), 4 * 8)