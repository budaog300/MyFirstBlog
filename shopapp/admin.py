from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview', 'time_create', 'photo', 'is_published')  # Отображение названий указанных столбцов
    list_display_links = ('id', 'title')  # Список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('title', 'preview', 'content')  # Поля, по которым можно будет производить поиск записей
    list_editable = ('is_published',)  # Чекбоксы, где мы можем убирать или ставить галочки


class ArticleStatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_article_name', 'views', 'date')
    list_display_links = ('id', 'views', 'get_article_name')
    search_fields = ('views', 'get_article_name')

    def get_article_name(self, obj):
        return obj.article.title if obj.article else 'Без названия'
    get_article_name.short_description = 'Название статьи'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'last_login', 'is_superuser', 'email', 'photo', 'is_active',
                    'is_staff', 'date_joined', 'first_name', 'last_name', 'date_birth')
    list_display_links = ('id', 'username', 'email')
    list_editable = ('is_superuser', 'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'date_birth', 'photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'message', 'time_create', 'ip_address', 'get_username')
    list_display_links = ('id', 'email', 'get_username')
    search_fields = ('first_name', 'email', 'get_username', 'ip_address',)

    def get_username(self, obj):
        return obj.user.username if obj.user else 'Anonymous'
    get_username.short_description = 'Логин'  # Установите заголовок столбца


class PostCommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'get_article_name', 'time_create', 'message')
    list_display_links = ('id', 'get_username', 'get_article_name')
    search_fields = ('get_username', 'get_article_name')

    def get_username(self, obj):
        return obj.user.username if obj.user else 'Пользователь удален'
    get_username.short_description = 'Логин'

    def get_article_name(self, obj):
        return obj.post.title if obj.post else 'Без названия'
    get_article_name.short_description = 'Название статьи'


admin.site.register(Women, WomenAdmin)
admin.site.register(ArticleStatistic, ArticleStatisticAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(PostComments, PostCommentsAdmin)
