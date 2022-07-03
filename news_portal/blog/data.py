# coding: utf-8

"""
    Модуль для автоматической генерации данных в базе.
    Используется в целях тестирования.
"""

import random
from .models import Author, User, Category, Post, Comment

users = [
    "Шекспир",
    "Байрон",
    "Вася"
]

authors = users[:2]

categories = [
    "Юмор",
    "Новости",
    "IT",
    "Сплетни"
]

article_text = """ 
По латыни профессор Richard McClintock - человек, которому приписывают открытие корни Lorem Ipsum - он, 
скорее всего, что когда-то в средние века наборщиком вскарабкался часть Цицерона De Finibus для того, 
чтобы предоставить текст-заполнитель для смоделируйте различных шрифтов для типа образца книги. 
Но это было только начало. """


def create_users():
    """ Создать трех пользователей (с помощью метода User.objects.create_user('username')). """
    for name in users:
        User.objects.create_user(username=name)
    print(User.objects.all())


def create_authors():
    """ Создать два объекта модели Author, связанные с пользователями. """
    for name in authors:
        Author.objects.create(user=User.objects.get_by_natural_key(username=name))
    print(Author.objects.all())


def create_categories():
    """ Добавить 4 категории в модель Category. """
    for category in categories:
        Category.objects.create(name=category)
    print(Category.objects.all())


def create_articles():
    """ Добавить 2 статьи и 1 новость.
        Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий). """
    article_authors = Author.objects.all()
    post = Post.objects.create(author=article_authors[0], title="Первая статья", text=article_text)
    post.category.add(Category.objects.get(id=3), Category.objects.get(id=1))
    post = Post.objects.create(author=article_authors[1], title="Вторая статья", text=article_text)
    post.category.add(Category.objects.get(id=2), Category.objects.get(id=3))
    news = Post.objects.create(author=article_authors[1], title="Первая новость",
                               post_type=Post.NEWS, text=article_text)
    news.category.add(Category.objects.get(id=4), Category.objects.get(id=1))
    print(Post.objects.all())


def add_comments():
    """ Создать как минимум 4 комментария к разным объектам модели Post
        (в каждом объекте должен быть как минимум один комментарий). """
    users = User.objects.all()
    posts = Post.objects.all()
    for user in users:
        for post in posts:
            text = f"{user.username} {random.choice(['одобряет', 'осуждает'])}"
            Comment.objects.create(post=post, user=user, text=text)


def like_dislike_posts_and_comments():
    """ Применяя функции like() и dislike() к статьям/новостям и
        комментариям, скорректировать рейтинги этих объектов. """
    for post in Post.objects.all():
        action = random.choice([post.like, post.like, post.dislike])    # Повысим шанс положительной оценки
        action()
    for comment in Comment.objects.all():
        action = random.choice([comment.like, comment.like, comment.dislike])   # Повысим шанс положительной оценки
        action()


def update_ratings():
    """ Обновить рейтинги пользователей. """
    for author in Author.objects.all():
        author.update_rating()


def print_ratings():
    """ Вывести рейтинги авторов. """
    print("\n======== Рейтинг авторов ==========")
    for author in Author.objects.all():
        print(f"{author.user.username}, rating={author.rating}")


def print_best_rating_author():
    """ Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта). """
    top_rating_author = Author.objects.order_by('-rating').first()
    print("\n======== Автор с самым высоким рейтингом ==========")
    print(f"{top_rating_author.user.username}, rating={top_rating_author.rating}")


def print_best_rating_article():
    """ Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
        основываясь на лайках/дислайках к этой статье.
        Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
    """
    post = Post.objects.order_by('-rating').first()
    print("\n======== Статья с самым высоким рейтингом ==========")
    print(f"Дата добавления: {post.date_time}\n"
          f"Автор: {post.author.user.username}\n"
          f"Рейтинг статьи: {post.rating}\n"
          f"Заголовок: {post.title}\n"
          f"Превью: {post.preview(length=128)}")


""" Создать записи в базе данных """
# create_users()
# create_authors()
# create_categories()
# create_articles()
# add_comments()
# for _ in range(5):
#     like_dislike_posts_and_comments()

""" Вывести результаты """
print_ratings()
update_ratings()
print_ratings()
print_best_rating_author()
print_best_rating_article()
