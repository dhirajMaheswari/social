from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('appSocial/login/', views.user_login, name = "user_login"),
    path('appSocial/logout/', views.user_logout, name='logout'),
    path('appSocial/signup/', views.user_signup, name='signup'),
    path('appSocial/success/', views.success, name='success'),
    path('appSocial/display/', views.display_images, name='display'),
    path('appSocial/display-user/', views.display_images_by_user, name='display_by_user'),
    path('appSocial/profile/<username>/', views.profile, name='profile'),
    path('appSocial/liked/<pk>/', views.liked, name='like'),
    path('appSocial/unliked/<pk>/', views.unliked, name='unlike'),
    path('appSocial/share/<pk>/',views.shared, name='shared'),
    path('appSocial/comment/<pk>/', views.comment_to_post, name='add_comment'),
    path('appSocial/like-comment/<ck>/', views.like_comment, name='like_comment'),
    path('appSocial/unlike-comment/<ck>/', views.unlike_comment, name='unlike_comment'),
    path('appSocial/com-ment/', views.comment_to_post, name='adding_comment'),
    path('appSocial/test/', views.test, name='test'),
    path('appSocial/test-ajax/', views.test_ajax, name='testaj'),

    # path('delete_items/<str:pk>', views.delete_items, name = "delete_items"),
]

#the "name" will be used to redirect urls as well as in html templates.

''' Note we also need to add the MEDIA_URL
if settings are in DEBUG mode, otherwise we won't be able to view uploaded images locally.
'''
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
