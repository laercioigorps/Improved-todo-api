from django.urls import path
from needs import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'needs'
urlpatterns = [
    path('need/', views.need_list_view, name='need_list'),
    path('need/<int:pk>/', views.need_detail_view, name='need_detail'),

    path('goal/', views.goal_list_view, name='goal_list'),
    path('<int:need>/goals/', views.goal_list_by_need_view,
         name='goal_list_by_need'),
    path('goal/<int:pk>/', views.goal_detail_view, name='goal_detail'),

    path('step/', views.step_list_view, name='step_list'),
    path('<int:goal>/steps/', views.step_list_by_goal_view,
         name='step_list_by_goal'),
    path('step/<int:pk>/', views.step_detail_view, name='step_detail'),

    path('iteration/', views.iteration_list_view, name='iteration_list'),
    path('iteration/<int:pk>/', views.iteration_detail_view,
         name='iteration_detail'),
    path('iteration/active/', views.iteration_get_active_view,
         name='active_iteration'),

    path('delivery/', views.delivery_list_view, name='delivery_list'),
    path('<int:goal>/delivery_by_goal/',
         views.delivery_list_by_goal_view, name='delivery_list_by_goal'),
    path('<int:step>/delivery/', views.delivery_list_by_step_view,
         name='delivery_list_by_step'),
    path('iteration/<int:iteration>/delivery/', views.delivery_list_by_iteration_view,
         name='delivery_list_by_iteration'),
    path('delivery/<int:pk>/', views.delivery_detail_view, name='delivery_detail'),
    path('wizard/', views.wizard_view, name='wizard'),

    path('tutorialsetup/', views.tutorial_setup_view, name='tutorial_setup'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
