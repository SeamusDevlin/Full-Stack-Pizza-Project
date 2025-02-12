from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('home', views.home, name='home'),
    path('menu', views.menu, name='menu'),
    path('payment', views.payment, name='payment'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('create/', views.create_pizza, name='create_pizza'),
    path('delivery/', views.delivery_details, name='delivery'),
    path('order/', views.order_confirmation, name='order'),
    path('history/', views.order_history, name='order_history'),
]