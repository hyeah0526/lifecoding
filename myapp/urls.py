from django.urls import path
from myapp import views

# 3-1. views를 임포트하고, path를 수정해주기 ---> views.index 

# http://127.0.0.1/
# http://127.0.0.1/app/

# http://127.0.0.1/create/

urlpatterns = [
    path('', views.index),   # 사용자가 home으로 들어왔따
    path('create/', views.create), #사용자가 create로 들어옴
    path('read/<id>/', views.read),
    path('update/<id>/', views.update),
    path('delete/', views.delete)
]
