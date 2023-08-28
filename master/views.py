from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework import status

from .models import Report, Feed, Scheme, FeedLike, FeedComment
from .serializers import ReportSerializer,FeedLikeSerializer,SchemeSerializer,FeedSerializer, FeedCommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# @api_view(['GET', 'POST', 'DELETE'])
# def report_list(request):
#     if request.method == 'GET':
#         reports = Report.objects.all()
        
#         title = request.query_params.get('title', None)
#         if title is not None:
#             reports = reports.filter(title__icontains=title)
        
#         reports_serializer = ReportSerializer(reports, many=True)
#         return JsonResponse(reports_serializer.data, safe=False)
#         # 'safe=False' for objects serialization
 
#     elif request.method == 'POST':
#         reports_data = JSONParser().parse(request)
#         reports_serializer = ReportSerializer(data=reports_data)
#         if reports_serializer.is_valid():
#             reports_serializer.save()
#             return JsonResponse(reports_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(reports_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         count = Report.objects.all().delete()
#         return JsonResponse({'message': '{} reports were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
# @api_view(['GET', 'PUT', 'DELETE'])
# def report_detail(request, pk):
#     try: 
#         report = Report.objects.get(pk=pk) 
#     except Report.DoesNotExist: 
#         return JsonResponse({'message': 'The report does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
#     if request.method == 'GET': 
#         report_serializer = ReportSerializer(report) 
#         return JsonResponse(report_serializer.data) 
 
#     elif request.method == 'PUT': 
#         report_data = JSONParser().parse(request) 
#         report_serializer = ReportSerializer(report, data=report_data) 
#         if report_serializer.is_valid(): 
#             report_serializer.save() 
#             return JsonResponse(report_serializer.data) 
#         return JsonResponse(report_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
#     elif request.method == 'DELETE': 
#         report.delete() 
#         return JsonResponse({'message': 'Report was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
# @api_view(['GET'])
# def report_list_published(request):
#     reports = Report.objects.filter(active="Solved")
        
#     if request.method == 'GET':
#         reports_serializer = ReportSerializer(reports, many=True)
#         return JsonResponse(reports_serializer.data, safe=False)

from rest_framework import generics

class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
    
class FeedListCreateView(generics.ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FeedRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    
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
def like_feed(request, feed_id):
    try:
        feed = Feed.objects.get(pk=feed_id)
    except Feed.DoesNotExist:
        return Response({"message": "Feed not found."}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    existing_like = FeedLike.objects.filter(user=user, feed=feed).first()
    if existing_like:
        return Response({"message": "You have already liked this feed."}, status=status.HTTP_400_BAD_REQUEST)

    FeedLike.objects.create(user=user, feed=feed)
    
    feed.likes = FeedLike.objects.filter(feed=feed, is_like=True).count()
    feed.save()
    serializer = FeedSerializer(feed)
    return Response({"message": "Feed liked successfully.", "data":serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, feed_id):
    try:
        feed = Feed.objects.get(pk=feed_id)
    except Feed.DoesNotExist:
        return Response({"message": "Feed not found."}, status=status.HTTP_404_NOT_FOUND)

    content = request.data.get('content', None)
    if not content:
        return Response({"message": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)

    comment = FeedComment.objects.create(user=request.user, feed=feed, content=content)
    serializer = FeedCommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
