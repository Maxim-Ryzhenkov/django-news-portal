from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    """ Модель описывает Автора """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __repr__(self):
        return f"Author (user.name='{self.user.username}', rating='{self.rating}')"

    def update_rating(self):
        """
        суммарный рейтинг каждой статьи автора умножается на 3;
        суммарный рейтинг всех комментариев автора;
        суммарный рейтинг всех комментариев к статьям автора.
        """
        posts_rating = self.posts.aggregate(result=Sum('rating')).get('result')
        comments_rating = self.user.comments.aggregate(result=Sum('rating')).get('result')
        print(f"===== {self.user.username}: обновляем рейтинг автора =====")
        print(f"Рейтинг постов = {posts_rating}")
        print(f"Рейтинг комментов = {comments_rating}")
        self.rating = 3 * posts_rating + comments_rating
        self.save()
        print(f"Рейтинг = 3 * {posts_rating} + {comments_rating} = {self.rating}")


class Category(models.Model):
    """ Категории новостей / статей — темы, которые
        они отражают(спорт, политика, образование и т.д.). """
    name = models.CharField(unique=True, max_length=128)

    def __repr__(self):
        return f"Category (name='{self.name}')"


class Post(models.Model):
    """ Модель содержит в себе статьи и новости, которые создают пользователи.
        Каждый объект может иметь одну или несколько категорий. """
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOISES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    date_time = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=2, choices=CATEGORY_CHOISES, default=ARTICLE)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __repr__(self):
        return f"Post (author.user.name='{self.author.user.username}', title='{self.title}', rating='{self.rating}'," \
               f"post_type='{self.post_type}')"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self, length=124):
        """ Вернуть превью статьи. """
        return f"{self.text[:length]}..." if len(self.text) > length else self.text


class PostCategory(models.Model):
    """ Промежуточная модель для связи «многие ко многим». """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """ Под каждой новостью/статьёй можно оставлять комментарии. """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
