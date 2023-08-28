from django.db import models
from django.conf import settings

# Create your models here.
REPORT_STATUS = (
    ("Pending", "Pending"),
    ("Solved", "Solved"),
)

post_STATUS = (
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
        
        
        
class Post(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    title           = models.TextField()
    image           = models.FileField(upload_to='uploads/posts',null=True,blank=True)
    video           = models.FileField(upload_to='uploads/posts',null=True,blank=True)
    tags            = models.CharField(max_length=50)
    likes           = models.IntegerField(default=0)
    address         = models.TextField()
    status          = models.CharField(max_length=20,choices=post_STATUS, default='Active')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'posts'
        
        
class PostLike(models.Model):
    user                =   models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    post                =   models.ForeignKey(Post, on_delete=models.CASCADE)
    is_like             =   models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} likes {self.post}"
    class Meta:
        db_table = 'post_likes'
    
class PostComment(models.Model):
    user                =   models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    post                =   models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    content             =   models.TextField()
    likes               =   models.PositiveIntegerField(default=0)
    created_at          =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
    class Meta:
        db_table = 'post_comments'

        
class Scheme(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    title           = models.TextField()
    tags            = models.CharField(max_length=50)
    image           = models.FileField(upload_to='uploads/posts',null=True,blank=True)
    video           = models.FileField(upload_to='uploads/posts',null=True,blank=True)
    address         = models.TextField()
    status          = models.CharField(max_length=20,choices=post_STATUS, default='Active')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'schemes'
        
class Announcement(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    title           = models.CharField(max_length=100)
    description     = models.TextField()
    status          = models.CharField(max_length=20,choices=post_STATUS, default='Active')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'announcements'