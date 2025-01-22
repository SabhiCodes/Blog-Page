from django.urls import path
from home.views import PublicBlog
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('blog/', PublicBlog.as_view(), name='public_blog'),
]

urlpatterns = format_suffix_patterns(urlpatterns)