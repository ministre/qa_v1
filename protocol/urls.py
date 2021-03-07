from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),
    path('create/', views.ProtocolCreate.as_view(), name='protocol_create'),
    path('update/<int:pk>/', views.ProtocolUpdate.as_view(), name='protocol_update'),
    path('status_update/<int:pk>/', views.ProtocolStatusUpdate.as_view(), name='protocol_status_update'),
    path('delete/<int:pk>/', views.ProtocolDelete.as_view(), name='protocol_delete'),
    path('<int:pk>/<int:tab_id>/', views.protocol_details, name='protocol_details'),
    # test results
    path('result/create/<int:protocol_id>/<int:test_id>/', views.result_create, name='result_create'),
    path('result/update/<int:pk>/', views.ResultUpdate.as_view(), name='result_update'),
    path('result/delete/<int:pk>/', views.ResultDelete.as_view(), name='result_delete'),
    path('result/<int:pk>/<int:tab_id>/', views.result_details, name='result_details'),
    # result notes
    path('result/note/create/<int:result>/', views.ResultNoteCreate.as_view(), name='result_note_create'),
    path('result/note/update/<int:pk>/', views.ResultNoteUpdate.as_view(), name='result_note_update'),
    path('result/note/delete/<int:pk>/', views.ResultNoteDelete.as_view(), name='result_note_delete'),
    # result configs
    path('result/config/create/<int:result>/', views.ResultConfigCreate.as_view(), name='result_config_create'),
    path('result/config/update/<int:pk>/', views.ResultConfigUpdate.as_view(), name='result_config_update'),
    path('result/config/delete/<int:pk>/', views.ResultConfigDelete.as_view(), name='result_config_delete'),
    # result images
    path('result/image/create/<int:result>/', views.ResultImageCreate.as_view(), name='result_image_create'),
    path('result/image/update/<int:pk>/', views.ResultImageUpdate.as_view(), name='result_image_update'),
    path('result/image/delete/<int:pk>/', views.ResultImageDelete.as_view(), name='result_image_delete'),
    # result files
    path('result/file/create/<int:result>/', views.ResultFileCreate.as_view(), name='result_file_create'),
    path('result/file/update/<int:pk>/', views.ResultFileUpdate.as_view(), name='result_file_update'),
    path('result/file/delete/<int:pk>/', views.ResultFileDelete.as_view(), name='result_file_delete'),
    # result issues
    path('result/issue/create/<int:result>/', views.ResultIssueCreate.as_view(), name='result_issue_create'),
    path('result/issue/update/<int:pk>/', views.ResultIssueUpdate.as_view(), name='result_issue_update'),
    path('result/issue/delete/<int:pk>/', views.ResultIssueDelete.as_view(), name='result_issue_delete'),
    # files
    path('file/create/<int:protocol_id>/', views.ProtocolFileCreate.as_view(), name='protocol_file_create'),
    path('file/update/<int:pk>/', views.ProtocolFileUpdate.as_view(), name='protocol_file_update'),
    path('file/delete/<int:pk>/', views.ProtocolFileDelete.as_view(), name='protocol_file_delete'),
    # additional issues
    path('issue/create/<int:protocol_id>/', views.ProtocolAdditionalIssueCreate.as_view(), name='protocol_issue_create'),
    path('issue/update/<int:pk>/', views.ProtocolAdditionalIssueUpdate.as_view(), name='protocol_issue_update'),
    path('issue/delete/<int:pk>/', views.ProtocolAdditionalIssueDelete.as_view(), name='protocol_issue_delete'),

    path('copy_results/', views.protocol_copy_results, name='protocol_copy_results'),
]
