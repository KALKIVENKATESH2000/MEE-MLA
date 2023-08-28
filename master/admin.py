from django.contrib import admin
from .models import Report, Feed, Scheme, FeedLike, FeedComment
# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Report._meta.get_fields()]
admin.site.register(Report, ReportAdmin)

class FeedAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Feed._meta.get_fields()]
admin.site.register(Feed, FeedAdmin)

class FeedLikeAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in FeedLike._meta.get_fields()]
admin.site.register(FeedLike, FeedLikeAdmin)

class FeedCommentAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in FeedComment._meta.get_fields()]
admin.site.register(FeedComment, FeedCommentAdmin)

class SchemeAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Scheme._meta.get_fields()]
admin.site.register(Scheme, SchemeAdmin)