from django.contrib import admin
from .models import Report, Post, Scheme, PostLike, PostComment, Announcement, Poll, Choice, Survey, Question, Answer
# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Report._meta.get_fields()]
admin.site.register(Report, ReportAdmin)

class PostAdmin(admin.ModelAdmin):
    # list_display =  [f.name for f in Post._meta.get_fields()]
    list_display = ["id", "title", "user", "image", "video", "tags", "likes", "address", "status", "createdAt", "updatedAt"]
admin.site.register(Post, PostAdmin)

class PostLikeAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in PostLike._meta.get_fields()]
admin.site.register(PostLike, PostLikeAdmin)

class PostCommentAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in PostComment._meta.get_fields()]
admin.site.register(PostComment, PostCommentAdmin)

class SchemeAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Scheme._meta.get_fields()]
admin.site.register(Scheme, SchemeAdmin)

class AnnouncementAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Announcement._meta.get_fields()]
admin.site.register(Announcement, AnnouncementAdmin)


class PollAdmin(admin.ModelAdmin):
    # list_display =  [f.name for f in Poll._meta.get_fields()]
    list_display = ["id", "question"]
admin.site.register(Poll, PollAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    # list_display =  [f.name for f in Choice._meta.get_fields()]
    list_display = ["id", "poll", 'text', 'votes']

admin.site.register(Choice, ChoiceAdmin)

class SurveyAdmin(admin.ModelAdmin):
    # list_display =  [f.name for f in Survey._meta.get_fields()]
    list_display = ["id", "title"]

admin.site.register(Survey, SurveyAdmin)


class QuestionAdmin(admin.ModelAdmin):
    # list_display =  [f.name for f in Question._meta.get_fields()]
    list_display = ["id", "survey", 'text']

admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Answer._meta.get_fields()]
    # list_display = ["id", "poll", 'text', 'votes']

admin.site.register(Answer, AnswerAdmin)