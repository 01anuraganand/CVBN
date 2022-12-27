from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('error/', views.error),
    path('architecture/', views.architecture),
    path('detect_disease/', views.render_upload_photo_classify, name = 'detect_disease'),
    path('upload_image/', views.render_upload_photo, name = 'upload_image'),
]