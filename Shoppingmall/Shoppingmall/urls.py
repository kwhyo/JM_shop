
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static 
from ckeditor_uploader import views as uploader_views



from django.contrib.auth.decorators import login_required
from ckeditor_uploader import views as views_ckeditor
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('sellers/', include('sellers.urls')),
    path('ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),
]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

