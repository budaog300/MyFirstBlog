from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *  # Импорт всех моделей
from .forms import AuthenticationForm, RegistrationForm, CustomUserProfileForm, UserPasswordChangeForm, \
    ContactMessageForm, PostCommentsForm
from django.contrib.auth.backends import BaseBackend
from django.contrib import messages
from django.db.models import Q, Sum
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import get_client_ip, paginate
from django.http import JsonResponse
import numpy as np

menu = [
    {'name': 'Главная страница', 'url_name': 'index'},
    {'name': 'О нас', 'url_name': 'about'},
    {'name': 'Контакты', 'url_name': 'contacts'},
    {'name': 'Статьи', 'url_name': 'article'},
    {'name': 'Войти/Зарегистрироваться', 'url_name': 'login'},
    {'name': 'Мой профиль', 'url_name': 'profile'},
]


def login_view(request):
    """ Авторизация """
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = request.POST.get('remember_me')
            user = authenticate(request, username=username, password=password)
            if user is None:
                try:
                    user = CustomUser.objects.get(email=username)
                    user = authenticate(request, username=user.username, password=password)
                except CustomUser.DoesNotExist:
                    pass
            if user is not None:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 недели
                else:
                    request.session.set_expiry(0)  # Закрыть при закрытии браузера
                return redirect('profile_pk', username=request.user.username)
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Неверный логин или пароль!'})
        else:
            errors = form.errors
            return render(request, 'registration/login.html', {'form': form, 'errors': errors})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'error': form.errors})


#
# def register(request):
#     """ Регистрация """
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             # user.is_active = True
#             user.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(request, username=username, password=password)
#             login(request, user)
#             return redirect('profile')
#         else:
#             errors = form.errors
#             print(form.errors)
#             return render(request, 'registration/register.html', {'form': form, 'errors': errors})
#     else:
#         form = RegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})


def register(request):
    """ Регистрация до подтверждения """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Подтверждение регистрации'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            from_email = 'kirillovdanila5@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            context = {
                'user': user
            }
            return render(request, 'registration/confirmation_sent.html', context)
        else:
            errors = form.errors
            return render(request, 'registration/register.html', {'form': form, 'errors': errors})
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    """ Регистрация после подтверждения """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='shopapp.backends.UserModelBackend')
        return redirect('profile_pk', username=request.user.username)
    else:
        return render(request, 'registration/activation_invalid.html')


def logout_view(request, next_page=None):
    """ Выход из системы """
    logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('login')


def index(request):
    """ Страница статей """
    posts = Women.objects.all()
    cats = Category.objects.all()
    users = CustomUser.objects.all()
    page_number = request.GET.get('page')
    if len(cats) == 0:
        raise Http404()
    context = {
        'users': users,
        'posts': posts,
        'cats': cats,
        'page_obj': paginate(request, posts, 3),
        'popular_posts': get_popular_posts(),
        'page_number': page_number,
    }
    return render(request, 'shopapp/index.html', context)


def profile(request, username):
    """ Страница профиля """
    users = CustomUser.objects.all()
    if username:
        user = get_object_or_404(CustomUser, username=username)
    else:
        user = request.user
    context = {
        'users': users,
        'username': username,
        'user': user
    }
    return render(request, 'shopapp/profile.html', context)


def update_profile(request):
    """ Обновление профиля """
    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    else:
        form = CustomUserProfileForm(instance=request.user)
    return render(request, 'shopapp/update_profile.html', {'form': form})


def about(request):
    """ Страница "О нас" """
    context = {

    }
    return render(request, 'shopapp/about.html', context)


def contacts(request):
    """ Страница контактов """
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.ip_address = get_client_ip(request)
            if request.user.is_authenticated:
                contact_message.user = request.user
            contact_message.save()
            messages.success(request,
                             'Ваше письмо успешно отправлено администрации сайта')  # сообщение об успешной отправке
            subject = f'Сообщение от пользователя {contact_message.first_name} {contact_message.last_name}, Почта отправителя: {contact_message.email}'
            message = render_to_string('registration/feedback_email_send.html', {
                'email': contact_message.email,
                'content': contact_message.message,
                'ip': contact_message.ip_address,
                'user': contact_message.user,
            })
            from_email = contact_message.email
            recipient_list = ['kirillovdanila5@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
            return redirect('contacts')
        else:
            errors = form.errors
            return render(request, 'shopapp/contacts.html', {'form': form, 'errors': errors})
    else:
        form = ContactMessageForm()
    return render(request, 'shopapp/contacts.html', {'form': form})


def show_category(request, cat_id):
    """ Страница одной категории """
    users = CustomUser.objects.all()
    query = request.GET.get('query')
    posts = Women.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()
    cat = get_object_or_404(Category, pk=cat_id)
    page_number = request.GET.get('page')
    if len(posts) == 0:
        raise Http404()
    context = { 
        'users': users,
        'posts': posts,
        'cats': cats,
        'cat': cat,
        'cat_id': cat_id,
        'page_obj': paginate(request, posts, 2),
        'page_number': page_number,
        'query': query,
        'popular_posts': get_popular_posts(),
    }
    return render(request, 'shopapp/category.html', context)


def all_posts(request):
    users = CustomUser.objects.all()
    query = request.GET.get('query')
    posts = Women.objects.filter(is_published=True)
    cats = Category.objects.all()
    page_number = request.GET.get('page')
    context = {
        'users': users,
        'posts': posts,
        'cats': cats,
        'page_obj': paginate(request, posts, 3),
        'page_number': page_number,
        'query': query,
        'popular_posts': get_popular_posts(),
    }
    return render(request, 'shopapp/includes/all_posts.html', context)


def search_results_view(request):
    """ Страница результата поиска """
    users = CustomUser.objects.all()
    posts = Women.objects.all()
    cats = Category.objects.all()
    query = request.GET.get('query')
    cat_id = request.GET.get('cat_id')
    page_number = request.GET.get('page')
    query = query.strip()
    if query:
        object_list = Women.objects.filter(
            Q(title__icontains=query) & Q(is_published=True)
        )

        if not object_list.exists():
            error = f'По вашему запросу "{query}" ничего не найдено!'
            context = {
                'users': users,
                'posts': posts,
                'cats': cats,
                'query': query,
                'cat_id': cat_id,
                'popular_posts': get_popular_posts(),
                'error': error
            }
            return render(request, 'shopapp/includes/search_results.html', context)
    else:
        object_list = Women.objects.none()  # Пустой QuerySet если нет запроса

    context = {
        'users': users,
        'posts': posts,
        'cats': cats,
        'object_list': object_list,
        'page_obj': paginate(request, object_list, 1),
        'page_number': page_number,
        'query': query,
        'cat_id': cat_id,
        'popular_posts': get_popular_posts()
    }
    return render(request, 'shopapp/includes/search_results.html', context)


def show_post(request, post_id):
    """ Страница одной статьи """
    users = CustomUser.objects.all()
    query = request.GET.get('query')
    posts = Women.objects.all()
    cats = Category.objects.all()
    post = get_object_or_404(Women, pk=post_id)
    page_number = request.GET.get('page')

    # Получение комментариев и их ответов
    comments = PostComments.objects.filter(post_id=post_id, parent__isnull=True).order_by('time_create')

    # Обработка статистики
    obj, created = ArticleStatistic.objects.get_or_create(
        defaults={
            "article": post,
            "date": timezone.now()
        },
        date=timezone.now(), article=post
    )
    obj.views += 1
    obj.save()

    # Обработка комментариев
    if request.method == 'POST':
        form = PostCommentsForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            parent_id = request.POST.get('parent_id', None)
            if parent_id:
                parent_comment = get_object_or_404(PostComments, id=parent_id)
                comment = PostComments.objects.create(post=post, user=request.user, message=message,
                                                      parent=parent_comment)
            else:
                comment = PostComments.objects.create(post=post, user=request.user, message=message)
            comment.save()
            return redirect(post.get_absolute_url())
        else:
            errors = form.errors
            return render(request, post.get_absolute_url(), {'form': form, 'errors': errors})
    else:
        form = PostCommentsForm()

    context = {
        'users': users,
        'posts': posts,
        'cats': cats,
        'post': post,
        'post_id': post_id,
        'page_number': page_number,
        'query': query,
        'popular_posts': get_popular_posts(),
        'form': form,
        'comments': comments,
        'page_obj': paginate(request, comments, 5),
    }
    return render(request, 'shopapp/post.html', context)


def get_popular_posts():
    """ Получить популярные статьи """
    return ArticleStatistic.objects.filter(date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]
                                           ).values(
        'article_id', 'article__title'
    ).annotate(
        total_views=Sum('views')
    ).order_by('-total_views')[:5]


def popular_posts(request):
    """ Страница популярных статей """
    posts = Women.objects.all()
    users = CustomUser.objects.all()
    context = {
        'posts': posts,
        'users': users,
        'popular_posts': get_popular_posts()
    }
    return render(request, 'shopapp/includes/popular_posts.html', context)


def users_view(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'shopapp/users_view.html', context)


def pageNotFound(request, exception):
    """ Страница ошибки 404 """
    return render(request, 'shopapp/404.html', status=404)


# Тестовое представление
def test_view(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'shopapp/includes/test.html', context)
