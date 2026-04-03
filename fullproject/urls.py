from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('destination', views.destination, name='destination'),
    path('gallery', views.gallery, name='gallery'),
    path('contact', views.contact, name='contact'),
    path('register', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('booking/', views.booking, name='booking'),
    path('fbooking/', views.fbooking, name='fbooking'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('success/<int:payment_id>/', views.success, name='success'),
    path('download-statement/<int:payment_id>/', views.download_statement, name='download_statement'),
    path('booking_history/', views.booking_history, name='booking_history'),
    # path('chatbot/', views.chatbot, name='chatbot'),
    # path('chatbot-api/', views.chatbot_api, name='chatbot_api'),

]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]