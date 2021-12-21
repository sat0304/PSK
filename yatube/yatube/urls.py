from django.contrib import admin

from django.urls import include, path


handler404 = 'core.views.page_not_found'
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
