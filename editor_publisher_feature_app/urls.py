from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from editor_publisher_feature_app.views.blog import blog_list_create, blog_update, blog_delete

urlpatterns = [
    # Route for listing all blogs and creating a new blog
    path('blogs/', blog_list_create, name='blog_list_create'),
    
    # Route for updating an existing blog
    path('blogs/update/<int:id>/', blog_update, name='blog_update'),
    
    # Route for deleting an existing blog
    path('blogs/delete/<int:id>/', blog_delete, name='blog_delete'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
