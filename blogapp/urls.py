from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('author/<name>', views.getauthor, name='author'),
    path('article/<int:id>', views.getsingle, name='single_post'),
    path('topic/<name>', views.gettopic, name='topic'),
    path('login', views.getlogin, name='login'),
    path('logout', views.getlogout, name='logout'),
    path('create', views.getcreate, name='create'),
    path('profile', views.getprofile, name='profile'),
    path('update/<int:id>', views.getupdate, name='update'),
    path('delete/<int:id>', views.getdelete, name='delete'),
    path('register', views.getregister, name='register'),
    path('topics', views.getCategory, name='category'),
    path('create/topic', views.createTopic, name='createTopic')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
