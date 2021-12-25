from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    template = 'core/404.html'
    context = {
        'path': request.path,
        'exception1': exception
    }
    return render(
        request, 
        template, 
        context,
        status=HTTPStatus.NOT_FOUND
    )

def csrf_failure(request, reason=''):
    template = 'core/403csrf.html'
    context = {
        'path': request.path,
        'reason1': reason
    }
    return render(
        request,
        template,
        context
    )

def server_error(request):
    template = 'core/500.html'
    return render(
        request,
        template,
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )

def permission_denied(request, exception):
    template = 'core/403.html'
    context = {
        'path': request.path,
        'exception1': exception
    }
    return render(
        request,
        template,
        status=HTTPStatus.FORBIDDEN
    )
