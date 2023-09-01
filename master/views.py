from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.views import APIView
from .models import Report, Post, Scheme, PostLike, PostComment, Announcement, Poll, Choice, Survey, Question, Answer, Event
from .serializers import ReportSerializer,postLikeSerializer,SchemeSerializer,PostSerializer,EventSerializer, PostCommentSerializer, AnnouncementSerializer, PollSerializer, ChoiceSerializer, SurveySerializer, QuestionSerializer, AnswerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from user.permissions import IsRegularUser, IsSuperuser
# Create your views here.


from rest_framework import generics

class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # permission_classes = [IsAuthenticated]

class ReportRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        permission_classes = [IsAuthenticated]
        serializer.save(user=self.request.user)

class UserReportsView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]       
    
    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)
    
    
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        permission_classes = [IsAuthenticated]
        serializer.save(user=self.request.user)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserReports(request):
    user = request.user
    
    reports = Report.objects.filter(user=user)
    serializer = ReportSerializer(reports)
    return Response({"message": "User  added reports.", "data":serializer.data}, status=status.HTTP_201_CREATED)

class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        if serializer.instance.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You don't have permission to update this post.")

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
            return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You don't have permission to delete this post.")
    
class SchemaListCreateView(generics.ListCreateAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    
    
    def perform_create(self, serializer):
        permission_classes = [IsAuthenticated]
        serializer.save(user=self.request.user)

class SchemaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    permission_classes = [IsAuthenticated]
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except post.DoesNotExist:
        return Response({"message": "post not found."}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    existing_like = PostLike.objects.filter(user=user, post=post).first()
    if existing_like:
        return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    PostLike.objects.create(user=user, post=post)
    
    post.likes = PostLike.objects.filter(post=post, is_like=True).count()
    post.save()
    serializer = PostSerializer(post)
    return Response({"message": "post liked successfully.", "data":serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except post.DoesNotExist:
        return Response({"message": "post not found."}, status=status.HTTP_404_NOT_FOUND)

    content = request.data.get('content', None)
    if not content:
        return Response({"message": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)

    comment = PostComment.objects.create(user=request.user, post=post, content=content)
    serializer = PostCommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



class AnnouncementListCreateView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    
    
    def perform_create(self, serializer):
        permission_classes = [IsAuthenticated]
        serializer.save(user=self.request.user)

class AnnouncementRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    
    
class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PollRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
  
    
class VoteView(generics.UpdateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        choice = self.get_object()
        user = request.user

        if user in choice.voters.all():
            raise PermissionDenied("You have already voted for this choice.")

        choice.votes += 1
        choice.voters.add(user)
        choice.save()
        
        return Response({"message": "Vote recorded successfully"}, status=status.HTTP_200_OK)


class SurveyList(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyDetail(generics.RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerDetail(generics.RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    

class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
# class CreateEvent(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             print("kkkkkkkkkkkkkkkkkkkkkkkk",serializer)
#             event = serializer.save(user=request.user)

#             access_token = request.data.get('access_token')  # Get the user's access token

#             service = build('calendar', 'v3', access_token=access_token)

#             event_result = service.events().insert(
#                 calendarId='primary',  # Change to the desired calendar ID
#                 body={
#                     'summary': event.event_name,
#                     'description': event.description,
#                     'start': {'dateTime': event.start_datetime.isoformat()},
#                     'end': {'dateTime': event.end_datetime.isoformat()},
#                     'conferenceData': {'createRequest': {'requestId': 'meet'}}
#                 }
#             ).execute()

#             event.meet_link = event_result.get('conferenceData', {}).get('entryPoints', [])[0].get('uri')
#             event.save()
#             print(event.meet_link)
#             return Response({'meet_link': event.meet_link})
#         return Response(serializer.errors)