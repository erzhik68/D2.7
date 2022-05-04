from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRate=Sum('post_rating'))
        pRat = 0
        pRat += postRat.get('postRate')
        comRat = self.author_user.comment_set.all().aggregate(commentRate=Sum('comment_rating'))
        cRat = 0
        cRat += comRat.get('commentRate')
        self.author_rating = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AT'
    TYPE_POST_CHOICES = [(NEWS, 'News'), (ARTICLE, 'Article'),]

    post_type = models.CharField(max_length=2, choices=TYPE_POST_CHOICES, default=NEWS)
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_date_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=100)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:123] + '...'

class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

