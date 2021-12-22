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
