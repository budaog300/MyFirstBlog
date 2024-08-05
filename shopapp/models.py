from django.db import models, connection
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Women(models.Model):
    """ Таблица Women """
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    preview = models.TextField(blank=True, verbose_name="Превью")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name="Категории")
    # objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_update', 'title']     # сортировка записей в админке и на сайте


class ArticleStatistic(models.Model):
    """ Таблица Статистика статей """
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    views = models.IntegerField(default=0, verbose_name="Просмотры")
    article = models.ForeignKey('Women', on_delete=models.CASCADE, null=True, verbose_name="Статья")  # внешний ключ на статью

    def __str__(self):
        return self.article.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.article.pk})

    class Meta:
        verbose_name = 'Статистика статей'
        verbose_name_plural = 'Статистика статей'
        db_table = 'PostStatistic'


class Category(models.Model):
    """ Таблица Категории """
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    # objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class CustomUser(AbstractUser):
    """ Таблица Пользователь """
    username = models.CharField(max_length=255, unique=True, verbose_name="Логин")
    password = models.CharField(max_length=255, unique=False, verbose_name="Пароль")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Последнее время вхождения")
    is_superuser = models.BooleanField(default=False, verbose_name="Superuser")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", verbose_name="Аватарка")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    first_name = models.CharField(max_length=255, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True, verbose_name="Фамилия")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")


class ContactMessage(models.Model):
    """ Таблица Сообщения """
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    email = models.EmailField(max_length=255, verbose_name="Email")
    message = models.TextField(max_length=1000, verbose_name="Сообщение")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP отправителя')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, verbose_name="Пользователь")

    def __str__(self):
        user_str = self.user.username if self.user else 'Пользователь удален'
        return f'{user_str} отправил письмо с {self.email}'

    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'
        db_table = 'message_contact'


class PostComments(models.Model):
    """ Таблица Комментарии к статье """
    message = models.TextField(max_length=1000, verbose_name="Комментарий")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата комментария")
    post = models.ForeignKey('Women', on_delete=models.CASCADE, null=True, verbose_name="Статья")
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies', verbose_name="Родитель")

    def __str__(self):
        user_str = self.user.username if self.user else 'Пользователь удален'
        post_str = self.post.title if self.post else 'Без названия'
        return f'{user_str}\'s Post- {post_str}'

    @property
    def children(self):
        return PostComments.objects.filter(parent=self).reverse()

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']
        db_table = 'post_comments'

