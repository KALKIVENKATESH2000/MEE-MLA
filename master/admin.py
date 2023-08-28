from django.contrib import admin
from .models import Report, Post, Scheme, PostLike, PostComment
# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Report._meta.get_fields()]
admin.site.register(Report, ReportAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Post._meta.get_fields()]
admin.site.register(Post, PostAdmin)

class PostLikeAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in PostLike._meta.get_fields()]
admin.site.register(PostLike, PostLikeAdmin)

class PostCommentAdmin(admin.ModelAdmin):
    # list_display =  [f.name for f in PostComment._meta.get_fields()]
    list_display = ["id"]
admin.site.register(PostComment, PostCommentAdmin)

class SchemeAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Scheme._meta.get_fields()]
admin.site.register(Scheme, SchemeAdmin)