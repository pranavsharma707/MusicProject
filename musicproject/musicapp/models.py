# from musicproject.musicproject.settings import BASE_DIR
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
import io
import wave
import contextlib
import os
from tinytag import TinyTag
from django.contrib.auth.models import User


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)

def mb(data):
    c=data/(1024*1024)
    return f"{c:.2f}MB"
# Create your models here.
CHOICE=[('Pop','Pop'),('Classic','Classic'),('Romantic','Romantic'),('Rock','Rock')]


class Category(models.Model):
    category_name=models.CharField(max_length=264,null=True,blank=True,choices=CHOICE)

   
    


class Singer(models.Model):
    singer_name=models.CharField(max_length=264,null=True,blank=True)

    

class Music(models.Model):
    title  =  models.CharField(max_length=264,null=True,blank=True)
    artist =  models.CharField(max_length=264,null=True,blank=True)
    size   =  models.CharField(max_length=264,null=True,blank=True)
    category_id  =  models.ForeignKey(Category,on_delete=models.CASCADE,default='')
    likes  =  models.ManyToManyField(User,related_name='music')
    # singer_id=models.ForeignKey(Singer,on_delete=models.CASCADE,default='')
    type   =  models.CharField(max_length=10,null=True,blank=True)
    album  =  models.CharField(max_length=264,null=True,blank=True)
    duration  =  models.CharField(max_length=50,null=True,blank=True)
    path   =  models.FileField(upload_to='music/')

    # def __str__(self):
    #     return self.title




@receiver(post_save,sender=Music)
def save_music(sender,instance,created,**kwargs):
    music=Music.objects.get(id=instance.id)
    file=settings.BASE_DIR
    path=music.path.url
    if created:
        tag=TinyTag.get(f"{file}{path}")
        instance.title=tag.title
        instance.artist=tag.artist
        instance.duration=convert(tag.duration)
        instance.album=tag.album
        instance.size=mb(tag.filesize)
        instance.save()    
post_save.connect(save_music,sender=Music)

class Comment(models.Model):
    music_id=models.ForeignKey(Music,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    reply=models.ForeignKey('Comment',null=True,related_name='replies',on_delete=models.CASCADE)
    comment=models.TextField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
   

# class Reply(models.Model):
#       music_id=models.ForeignKey(Music,on_delete=models.CASCADE)
#       user_id=models.ForeignKey(User,on_delete=models.CASCADE)
#       comment_id=models.ForeignKey(Comment,on_delete=models.CASCADE)
#       reply=models.TextField(null=True,blank=True)
#       created_on = models.DateTimeField(auto_now_add=True)
#       user_reply=models.CharField(null=True,blank=True,max_length=256,default='')

      
     



    







