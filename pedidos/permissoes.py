from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test


def grupo_requerido(nome_grupo):
    """
    Decorator para exigir que o usuário pertença a um grupo específico.
    """
    def decorator(view_func):
        @login_required
        @user_passes_test(lambda u: u.groups.filter(name=nome_grupo).exists(), login_url='login')
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def somente_staff(view_func):
    """
    Decorator que permite acesso apenas a usuários staff (is_staff=True).
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Você não tem permissão para acessar esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def somente_superuser(view_func):
    """
    Decorator que permite acesso apenas a superusuários (is_superuser=True).
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Apenas superusuários podem acessar esta funcionalidade.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def somente_proprietario(get_obj_func):
    """
    Decorator para permitir acesso somente ao proprietário de um objeto específico.
    Exemplo de uso:

        @somente_proprietario(lambda request, pk: Pedido.objects.get(pk=pk))
        def minha_view(request, pk):
            ...

    """
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            objeto = get_obj_func(request, *args, **kwargs)
            if objeto.usuario != request.user:
                raise PermissionDenied("Você não tem permissão para acessar este item.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
