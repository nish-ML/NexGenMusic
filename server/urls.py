from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
	path("", TemplateView.as_view(template_name="home.html"), name="home"),
	path("register/", TemplateView.as_view(template_name="register.html"), name="register-page"),
	path("login/", TemplateView.as_view(template_name="login.html"), name="login-page"),
	path("generate/", TemplateView.as_view(template_name="generate.html"), name="generate-page"),
	path("history/", TemplateView.as_view(template_name="history.html"), name="history-page"),
	path("admin/", admin.site.urls),
	path("api/", include("api.urls")),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


