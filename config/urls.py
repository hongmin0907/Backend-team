from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
       title="Snippets API",
       default_version='v1',
       description="Test description",
       terms_of_service="https://www.google.com/policies/terms/",
       contact=openapi.Contact(email="contact@snippets.local"),
       license=openapi.License(name="BSD License"),
   ),
   validators=['flex'],
   # validators=['ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('stay/', include('stay.urls')),
    path('api/get_token/', obtain_auth_token),
    path('search/',include('search.urls')),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns