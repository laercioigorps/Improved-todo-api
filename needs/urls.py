from django.urls import path
from needs import views

urlpatterns = [
    path('need/', views.need_list_view),
    path('need/<int:pk>/', views.need_detail_view),
    path('goal/', views.goal_list_view),
    path('goal/<int:pk>/', views.goal_detail_view)
]
