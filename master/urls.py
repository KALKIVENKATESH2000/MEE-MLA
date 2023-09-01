from django.urls import path
# from master import views 
 
# urlpatterns = [ 
#     path('reports/', views.report_list),
#     path('reports/<str:pk>/', views.report_detail),

#     # url(r'^api/tutorials$', views.tutorial_list),
#     # url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
#     # url(r'^api/tutorials/published$', views.tutorial_list_published)
# ]

from .views import *

urlpatterns = [
    path('reports/', ReportListCreateView.as_view(), name='reports-list-create'),
    path('reports/<int:pk>/', ReportRetrieveUpdateDeleteView.as_view(), name='report-retrieve-update-delete'),
    path('reports/user/', UserReportsView.as_view(), name='reports-by-user'),
    path('posts/', PostListCreateView.as_view(), name='posts-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-retrieve-update-delete'),
    path('schemas/', SchemaListCreateView.as_view(), name='schemas-list-create'),
    path('schemas/<int:pk>/', SchemaRetrieveUpdateDeleteView.as_view(), name='schema-retrieve-update-delete'),
    path('posts/<int:post_id>/like/', like_post, name='like-post'),
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
    
    
    # path('events/', EventList.as_view(), name='event-list'),
    # path('create-meet/', CreateEvent.as_view(), name='create-meet'),

]