from django.db import models


class User(models.Model):
    """ Модель пользователя """
    username = models.Model()
    full_name = models.TextField
    registration_date = models.DateField(auto_created=True)
    email = models.EmailField()
    is_author = models.BooleanField(default=False)


class Category(models.Model):
    """ Модель категории записи """
    name = models.CharField(max_length=50)


class Post(models.Model):
    """ Модель записи - поста """
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, through='PostCategory')


class PostCategory(models.Model):
    """ Таблица связи постов и категорий. """
    post = models.ForeignKey(Post, on_delete=)
    category = models.ForeignKey(Category, on_delete=)