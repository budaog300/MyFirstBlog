from django.core.paginator import Paginator


def get_client_ip(request):
    """
    Get user's IP
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip


def paginate(request, model, count):
    """ Пагинатор """
    paginator = Paginator(model, count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
