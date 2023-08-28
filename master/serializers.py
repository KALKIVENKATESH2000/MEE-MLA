from rest_framework import serializers 
from .models import Report, Post, Scheme, PostLike, PostComment
from user.serializers import UserSerializer
 
 
class ReportSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Report
        fields = "__all__"
        
class PostCommentSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = PostComment
        fields = "__all__"
                
class PostSerializer(serializers.ModelSerializer):
    comments = PostCommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        

class SchemeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Scheme
        fields = "__all__"
        
        
class postLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"
        
