from rest_framework import serializers 
from .models import Report, Feed, Scheme, FeedLike, FeedComment
from user.serializers import UserSerializer
 
 
class ReportSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Report
        fields = "__all__"
        
class FeedCommentSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = FeedComment
        fields = "__all__"
                
class FeedSerializer(serializers.ModelSerializer):
    comments = FeedCommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Feed
        fields = "__all__"
        

class SchemeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Scheme
        fields = "__all__"
        
        
class FeedLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedLike
        fields = "__all__"
        
