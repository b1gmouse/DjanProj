from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += post_rating.get('postRating')

        comment_rating = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += comment_rating.get('commentRating')

        self.rating_author = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=32, unique = True)



class Post(models.Model):
    News = 'NW'
    Article = 'AR'
    variables = (
        (News, 'Новости'),
        (Article, 'Статьи')
    )
    post = models.ForeignKey(Author, on_delete = models.CASCADE)
    choice = models.CharField(max_length=2, choices=variables, default=Article)
    date_creation = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=32)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + "..."




class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete = models.CASCADE)
    categories = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    com_to_post = models.ForeignKey(Post, on_delete = models.CASCADE)
    com_to_user = models.ForeignKey(User, on_delete = models.CASCADE)
    commentary = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

