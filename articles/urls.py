from django.urls import path
from articles.views import main_view, save_file, welcome_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
  path('', welcome_view, name="welcome"),
  path('index/save/', save_file, name="save"),
  path('index/', main_view, name="home")
]

urlpatterns += staticfiles_urlpatterns()