from django.contrib import admin
from django.conf import settings

from django.urls import include, path


handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'
urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'about/',
        include(
            'about.urls',
            namespace='about'
        )
    ),
    path(
        'auth/',
        include(
            'users.urls',
            namespace='users'
        )
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
    path(
        '',
        include(
            'posts.urls',
            namespace='posts'
        )
    ),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
