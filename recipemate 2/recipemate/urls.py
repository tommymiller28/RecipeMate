from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from recipes import views  # Import views from the recipes app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Set the home view as the default
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  # Custom registration view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

