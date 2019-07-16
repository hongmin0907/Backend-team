from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_swagger_view(title='Yanolja API Document')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('stay/', include('stay.urls')),
    path('api/doc/', schema_view),
    path('api/get_token/', obtain_auth_token),
    path('search/',include('search.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)