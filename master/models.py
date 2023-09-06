from django.db import models
from django.conf import settings
from user.models import CustomUser

# Create your models here.
REPORT_STATUS = (
    ("failed", "Failed"),
    ("pending", "Pending"),
    ("solved", "Solved"),
)

REPORT_PRIORITY = (
    ("low", "Low"),
    ("normal", "Normal"),
    ("high", "High"),
    ("urgent", "Urgent"),
)

post_STATUS = (
    ("Active", "Active"),
    ("Inactive", "Inactive"),
    ("Deleted", "Deleted"),
)



def upload(instance, filename):
    return 'uploads/folder/{filename}'.format(filename=filename)

class Report(models.Model):
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    full_name       = models.CharField(max_length=150)
    email           = models.CharField(max_length=50)
    mobile_no       = models.CharField(max_length=150)
    pincode         = models.IntegerField()
    city            = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    address         = models.TextField()
    report          = models.TextField()
    report_image    = models.FileField(upload_to='uploads/reports',null=True,blank=True)
    reporter_selfie = models.FileField(upload_to='uploads/reports',null=True,blank=True)
    priority        = models.CharField(max_length=20,choices=REPORT_PRIORITY, default='normal')
    status          = models.CharField(max_length=20,choices=REPORT_STATUS, default='pending')
    mla_response    = models.CharField(max_length=150, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report +'by'+ self.full_name
    class Meta:
        db_table = 'reports'
        
        
        
class Post(models.Model):
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    title           = models.TextField()
    image           = models.FileField(upload_to='uploads/posts',null=True,blank=True)
    video           = models.FileField(upload_to='uploads/posts',null=True,blank=True)
    tags            = models.ManyToManyField(CustomUser, related_name='tagged_in_posts', null=True,blank=True)
    likes           = models.IntegerField(default=0)
    pincode         = models.CharField(max_length=50, null=True)
    city            = models.CharField(max_length=50, null=True)
    state           = models.CharField(max_length=50, null=True)
    status          = models.CharField(max_length=20,choices=post_STATUS, default='Active')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'posts'
        
        
class PostLike(models.Model):
    user                =   models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    post                =   models.ForeignKey(Post, on_delete=models.CASCADE)
    is_like             =   models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} likes {self.post}"
    class Meta:
        db_table = 'post_likes'
    
class PostComment(models.Model):
    user                =   models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    post                =   models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    content             =   models.TextField()
    likes               =   models.PositiveIntegerField(default=0)
    created_at          =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
    class Meta:
        db_table = 'post_comments'

        
class Scheme(models.Model):
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    title           = models.CharField(max_length=250)
    description     = models.TextField()
    tags            = models.CharField(max_length=50,null=True,blank=True)
    image           = models.FileField(upload_to='uploads/posts',null=True,blank=True)
    video           = models.FileField(upload_to='uploads/posts',null=True,blank=True)
    pincode         = models.CharField(max_length=50, null=True)
    city            = models.CharField(max_length=50, null=True)
    state           = models.CharField(max_length=50, null=True)    
    status          = models.CharField(max_length=20,choices=post_STATUS, default='Active')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'schemes'
        
class Announcement(models.Model):
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    title           = models.CharField(max_length=100)
    description     = models.TextField()
    status          = models.CharField(max_length=20,choices=post_STATUS, default='Active')
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'announcements'
        
        
class Poll(models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question
    
    class Meta:
        db_table = 'polls'

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'poll_choices'

class UserVote(models.Model):
    user    = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    choice  = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'choice')


class Survey(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'surveys'
class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'survey_questions'
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'survey_answers'


def generate_meet_link(event):
    meet_domain = "https://meet.google.com/"
    
    event_name_slug = event.event_name.replace(" ", "-").lower()
    # Format the start and end times properly
    start_time = event.start_datetime.strftime("%Y%m%dT%H%M%S")
    end_time = event.end_datetime.strftime("%Y%m%dT%H%M%S")
    
    # Remove any non-alphanumeric characters from the slug
    sanitized_event_name_slug = ''.join(c for c in event_name_slug if c.isalnum() or c == '-')
    
    meeting_code = f"{sanitized_event_name_slug}-{start_time}-{end_time}"
    
    return f"{meet_domain}{meeting_code}"

class Event(models.Model):
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    event_name = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    description = models.TextField()
    meet_link = models.URLField(blank=True, null=True)  # Google Meet link

    def __str__(self):
        return self.event_name
    
    def save(self, *args, **kwargs):
        if not self.meet_link:
            self.meet_link = generate_meet_link(self)
        super().save(*args, **kwargs)

class Constituency(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name