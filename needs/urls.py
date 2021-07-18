from django.urls import path
from needs import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('need/', views.need_list_view),
    path('need/<int:pk>/', views.need_detail_view),
    path('goal/', views.goal_list_view),
    path('goal/<int:pk>/', views.goal_detail_view),
    path('step/', views.step_list_view),
    path('step/<int:pk>/', views.step_detail_view),
    path('iteration/', views.iteration_list_view),
    path('iteration/<int:pk>/', views.iteration_detail_view),
    path('delivery/', views.delivery_list_view),
    path('delivery/<int:pk>/', views.delivery_detail_view),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
