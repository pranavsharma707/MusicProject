from django.contrib import admin
from django.db import models
from .models import Music,Singer,Category,Comment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display=['id','music_id','user_id','comment','reply']

# class ReplyAdmin(admin.ModelAdmin):
#     list_display=['id','music_id','user_id','reply','user_reply']

admin.site.register(Music)
admin.site.register(Singer)
admin.site.register(Category)
admin.site.register(Comment,CommentAdmin)
# admin.site.register(Reply,ReplyAdmin)
