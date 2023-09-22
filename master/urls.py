from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('reports/', ReportListCreateView.as_view(), name='reports-list-create'),
    path('reports/<int:pk>/', ReportRetrieveUpdateDeleteView.as_view(), name='report-retrieve-update-delete'),
    path('reports/user/', UserReportsView.as_view(), name='reports-by-user'),
    path('reports/<int:id>/status/', report_status_update, name='report-status-update'),
    path('reports/count/', ReportListCountView.as_view(), name='reports-count'),
    path('posts/', PostListCreateView.as_view(), name='posts-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-retrieve-update-delete'),
    path('schemas/', SchemaListCreateView.as_view(), name='schemas-list-create'),
    path('schemas/<int:pk>/', SchemaRetrieveUpdateDeleteView.as_view(), name='schema-retrieve-update-delete'),
    path('posts/<int:post_id>/like/', like_post, name='like-post'),
    path('posts/user_liked', UserLikedPostsView.as_view(), name='like-status'),
    path('posts/<int:post_id>/comments/', create_comment, name='create-comment'),
    path('annocements/', AnnouncementListCreateView.as_view(), name='annocements-list-create'),
    path('annocements/<int:pk>/', AnnouncementRetrieveUpdateDeleteView.as_view(), name='annocements-retrieve-update-delete'),
    path('polls/', PollList.as_view(), name='poll-list'),
    path('polls/vote/<int:pk>/', VoteView.as_view(), name='vote'),
    path('polls/<int:pk>/', PollRetrieveUpdateDestroyView.as_view(), name='poll-detail'),
    
    path('surveys/', SurveyList.as_view(), name='survey-list'),
    path('surveys/<int:pk>/', SurveyDetail.as_view(), name='survey-detail'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('answers/<int:pk>/', AnswerDetail.as_view(), name='answer-detail'),
    
    path('voters/upload/', VoterUploadView.as_view(), name='voter-upload'),
    path('voters/re-upload/', VoterReUploadView.as_view(), name='voter-re_upload'),
    # path('voters/list/export/', VotersListDownloadView.as_view(), name='voter-list-export'),
    path('voters/list/export/<int:polling_station>', VotersListDownloadView, name='voter-list-export'),
    path('voters/', VoterListCreate.as_view(), name='voter-list-create'),
    path('voters/<int:pk>/', VoterRetrieveUpdateDeleteView.as_view(), name='voter-update-detail-delete'),
    
    # path('events/', EventList.as_view(), name='event-list'),
    # path('create-meet/', CreateEvent.as_view(), name='create-meet'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)