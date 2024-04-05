from django.db import models
from datetime import date
from django.contrib.auth.models import User


# class User(models.Model):
# login = models.CharField(max_length=200)
# email = models.EmailField()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        posts_rating = 0
        comments_rating = 0
        posts_conmments_rating = 0
        posts = Post.objects.filter(author=self)
        for p in posts:
            posts_rating += p.rating
        comments = Comment.objects.filter(user=self.user)
        for c in comments:
            comments_rating += c.rating
        posts_comments = Comment.objects.filter(post__author=self)
        for pc in posts_comments:
            posts_conmments_rating += pc.rating

        self.rating = posts_rating * 3 + comments_rating + posts_conmments_rating

        self.save()

    def top(self):
        username = Author.objects.all().order_by('-rating').values('user')
        keys = list(username.keys())
        print (keys[0])

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    DECIDE = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(choices=DECIDE, max_length=255, default=news)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        small_text = self.text[0:124] + '...'
        return small_text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


from django.db import models

# Create your models here.
