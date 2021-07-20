from django.urls import path
from needs import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'needs'
urlpatterns = [
    path('need/', views.need_list_view, name='need_list'),
    path('need/<int:pk>/', views.need_detail_view, name='need_detail'),
    path('goal/', views.goal_list_view, name='goal_list'),
    path('goal/<int:pk>/', views.goal_detail_view, name='goal_detail'),
    path('step/', views.step_list_view, name='step_list'),
    path('step/<int:pk>/', views.step_detail_view, name='step_detail'),
    path('iteration/', views.iteration_list_view, name='iteration_list'),
    path('iteration/<int:pk>/', views.iteration_detail_view, name='iteration_detail'),
    path('delivery/', views.delivery_list_view, name='delivery_list'),
    path('delivery/<int:pk>/', views.delivery_detail_view, name='delivery_detail'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
