from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework import status

from .models import Report, Post, Scheme, PostLike, PostComment
from .serializers import ReportSerializer,postLikeSerializer,SchemeSerializer,PostSerializer, PostCommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

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
    
    
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        permission_classes = [IsAuthenticated]
        serializer.save(user=self.request.user)

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
