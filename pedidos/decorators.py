from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from functools import wraps

def login_required_if_not_debug(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if settings.DEBUG:
            # DEBUG = True: injeta usuário mock no request para testes
            if not request.user.is_authenticated:
                # Busca ou cria um usuário para teste (exemplo: id=1)
                user, created = User.objects.get_or_create(username='testuser', defaults={'password': '12345'})
                # Substitui request.user para view
                request.user = user
            return view_func(request, *args, **kwargs)
        else:
            # DEBUG = False: exige login
            decorated_view = login_required(view_func)
            return decorated_view(request, *args, **kwargs)
    return _wrapped_view
