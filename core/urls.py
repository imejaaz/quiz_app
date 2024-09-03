from rest_framework import permissions
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Define the schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('account.urls')),
    path('quiz/', include('quiz.urls')),
    #     path('swagger/', schema_view.with_ui('swagger',
    #          cache_timeout=0), name='schema-swagger-ui'),
]
