from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve
from app import views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from app.views import robots_txt
from app.sitemaps import StaticViewSitemap
sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loading, name='loading'),
    path('home/', views.home, name='home'),
    path('destination/', views.destination, name='destination'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('booking/', views.booking, name='booking'),
    path('fbooking/', views.fbooking, name='fbooking'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('profile/', views.profile, name='profile'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('success/<int:payment_id>/', views.success, name='success'),
    path('download-statement/<int:payment_id>/', views.download_statement, name='download_statement'),
    path('booking_history/', views.booking_history, name='booking_history'),
    # path('chatbot/', views.chatbot, name='chatbot'),
    # path('chatbot-api/', views.chatbot_api, name='chatbot_api'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
    ),
]
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)