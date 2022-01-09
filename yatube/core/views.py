from http import HTTPStatus

from django.shortcuts import render, render_to_response


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
        context,
        status=HTTPStatus.FORBIDDEN
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
        context,
        status=HTTPStatus.FORBIDDEN
    )
    
def handler403(request, *args, **argv):
    print('Handler 403 was called!')
    u = request.user
    params = {
        'user': u,
    }
    response = render_to_response('core/403.html', params)
    response.status_code = HTTPStatus.FORBIDDEN
    return response
