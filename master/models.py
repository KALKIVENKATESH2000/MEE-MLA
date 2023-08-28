from django.db import models
from django.conf import settings

# Create your models here.
REPORT_STATUS = (
    ("Pending", "Pending"),
    ("Solved", "Solved"),
)

FEED_STATUS = (
    ("Active", "Active"),
    ("Inactive", "Inactive"),
    ("Deleted", "Deleted"),
)



def upload(instance, filename):
    return 'uploads/folder/{filename}'.format(filename=filename)

class Report(models.Model):
    full_name       = models.CharField(max_length=150)
    email           = models.CharField(max_length=50)
    mobile_no       = models.CharField(max_length=150)
    pincode         = models.IntegerField()
    city            = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    address         = models.TextField()
    report          = models.TextField()
    status          = models.CharField(max_length=20,choices=REPORT_STATUS, default='Pending')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report +'by'+ self.full_name
    class Meta:
        db_table = 'reports'
        
        
        
class Feed(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    title           = models.TextField()
    image           = models.FileField(upload_to='uploads/feeds',null=True,blank=True)
    video           = models.FileField(upload_to='uploads/feeds',null=True,blank=True)
    likes           = models.IntegerField(default=0)
    address         = models.TextField()
    status          = models.CharField(max_length=20,choices=FEED_STATUS, default='Active')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'feeds'
        
        
class FeedLike(models.Model):
    user                =   models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    feed                =   models.ForeignKey(Feed, on_delete=models.CASCADE)
    is_like             =   models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} likes {self.feed}"
    class Meta:
        db_table = 'feed_likes'
    
class FeedComment(models.Model):
    user                =   models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    feed                =   models.ForeignKey(Feed, on_delete=models.CASCADE,related_name='comments')
    content             =   models.TextField()
    likes               =   models.PositiveIntegerField(default=0)
    created_at          =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.feed.title}"
    class Meta:
        db_table = 'feed_comments'

        
class Scheme(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    title           = models.TextField()
    image           = models.FileField(upload_to='uploads/feeds',null=True,blank=True)
    video           = models.FileField(upload_to='uploads/feeds',null=True,blank=True)
    address         = models.TextField()
    status          = models.CharField(max_length=20,choices=FEED_STATUS, default='Active')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'schemes'