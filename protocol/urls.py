from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),
    path('create/', views.ProtocolCreate.as_view(), name='protocol_create'),
    path('update/<int:pk>/', views.ProtocolUpdate.as_view(), name='protocol_update'),
    path('delete/<int:pk>/', views.ProtocolDelete.as_view(), name='protocol_delete'),
    path('<int:pk>/<int:tab_id>/', views.protocol_details, name='protocol_details'),


    path('result/update/<int:pk>/', views.ResultUpdate.as_view(), name='result_update'),
    path('result/<int:pk>/<int:tab_id>/', views.result_details, name='result_details'),
    # configs
    path('result/config/create/<int:result>/', views.ResultConfigCreate.as_view(), name='result_config_create'),
    path('result/config/update/<int:pk>/', views.ResultConfigUpdate.as_view(), name='result_config_update'),
    path('result/config/delete/<int:pk>/', views.ResultConfigDelete.as_view(), name='result_config_delete'),
    # issues
    path('result/issue/create/<int:result>/', views.ResultIssueCreate.as_view(), name='result_issue_create'),
    path('result/issue/update/<int:pk>/', views.ResultIssueUpdate.as_view(), name='result_issue_update'),
    path('result/issue/delete/<int:pk>/', views.ResultIssueDelete.as_view(), name='result_issue_delete'),

    # path('restore_configs/<int:pk>/', views.restore_configs, name='restore_configs'),
    # path('delete_configs/<int:pk>/', views.delete_configs, name='delete_configs'),


    path('import/', views.protocol_import, name='protocol_import'),
    path('copy_results/', views.protocol_copy_results, name='protocol_copy_results'),
]
