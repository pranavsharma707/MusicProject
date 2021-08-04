from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
import music_tag
from django import http
from tinytag import TinyTag
from hurry.filesize import size
from musicapp.models import Music,Category,Singer,Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from musicapp.forms import CreateUserForm
from django.http import HttpResponseRedirect,JsonResponse
from django.db.models import Q
import json
from django.core import serializers


import wave
import contextlib
import os

@login_required(login_url='/login/')
def home(request):
   if request.method=='POST':
      file=request.FILES['musicupload']  
      data=str(file)     
      category=Category.objects.get(category_name=request.POST['category'])
      singer=Singer.objects.get(singer_name=request.POST['singer'])
      audio=Music(category_id=category,singer_id=singer,path=file,type=data[-3:])
      audio.save()
      return render(request,'music/submit.html')
   return render(request,'music/submit.html')


@login_required(login_url='/login/')
def show(request):
   music=Music.objects.all()
   return render(request,'music/show.html',{'music':music})

# @login_required(login_url='/login/')
# def play(request, id):
#    if request.method=='GET':
#           audio=Music.objects.filter(id=id)
#           comment=Comment.objects.filter(music_id__in=audio,reply=None).order_by('-id')
#        #    reply=Reply.objects.filter(comment_id__in=comment)
#           count=comment.count()
#           return render(request,'music/play.html',{'audio':audio,'comment':comment,'count':count})
#    else:
#               user=request.user
#               comment=request.POST['comment']
#               music=request.POST['music_id']
#               reply_id=request.POST.get('comment_id',None)
#               print(reply_id)
#               audio=Music.objects.get(id=music)
#               reply_data=None
#               if reply_id:
#                      reply_data=Comment.objects.get(id=reply_id)
#               comment=Comment(user_id=user,music_id=audio,comment=comment,reply=reply_data)
#               comment.save()
#               return redirect('play',id=audio.id)
          

def register(request):
       if request.method=='POST':
              username=request.POST['username']
              password=request.POST['password']


              try:
                 user=User.objects.get(username=username)
                 print(user.email)
              except User.DoesNotExist:
                 user=User.objects.create_user(username=username,password=password)
                 user.save()
                 messages.success(request,'user register successfully now you can login')
                 return render(request,'music/register.html')
              else:
                     messages.error(request,'please choose a unique username')
                     return render(request,'music/register.html')
       return render(request,'music/register.html')

def user_login(request):
       if request.method=='POST':
               username=request.POST['username']
               password=request.POST['password']
               user=authenticate(username=username,password=password)
               if user is not None:
                     login(request,user)
                     messages.success(request,'user login successfully')
                     return redirect('home')
               else:
                      messages.error(request,'invalid username/password')
                      return render(request,'music/login.html')
       return render(request,'music/login.html')


@login_required(login_url='login/')
def user_logout(request):
       logout(request)
       return render(request,'music/login.html')


# def user_form(request):
#        user=CreateUserForm()
#        if request.method=='POST':
#               creater_user=CreateUserForm(request.POST)
#               if creater_user.is_valid():
#                      creater_user.save()
#                      return render(request,'music/user.html',{'user':user})

#        return render(request,'music/user.html',{'user':user})
              

def comment(request,id):
      if request.method=='POST':
             user=request.user
             comment=request.POST['comment']
             music=request.POST['music_id']
             audio=Music.objects.get(id=music)
             comment=Comment(user_id=user,music_id=audio,comment=comment)
             comment.save()
             return redirect('comment',id=audio.id)
      else:
             audio=Music.objects.filter(id=id)
             print(audio)
             comment=Comment.objects.filter(music_id__in=audio)
             print(comment)
             return render(request,'music/comment.html',{'comment':comment,'music':audio})

# def likes(request,pk):
#        music=get_object_or_404(Music,id=request.POST.get('music_id'))
#        print('likes',request.user)
#        if music.likes.filter(id=request.user.id).exists():
#                  music.likes.remove(request.user)
#        else:
#               music.likes.add(request.user)

#        return HttpResponseRedirect(reverse('play', args=[str(pk)]))

#using jquery
def likes(request):
       if request.method=='POST':
              if request.POST.get("operation")=='like_submit' and request.is_ajax():
                     print(request.user)
                     music_id=request.POST.get("music_id",None)
                     music=get_object_or_404(Music,pk=music_id)
                     if music.likes.filter(id=request.user.id).exists():
                                music.likes.remove(request.user)
                     else:
                          music.likes.add(request.user)
                     data=music.likes.count()
                     # return HttpResponseRedirect(reverse('play', args=[str(music_id)]))
                     return JsonResponse(data,safe=False)



# def reply(request):
#        if request.method=='POST' or request.method=='GET':     
#        #        audio=Music.objects.filter(id=id)
#        #        reply=Reply.objects.filter(music_id__in=audio)
#        #        return render(request,'music/play.html',{'audio':audio})
#        # else:
#              user=request.user
#              reply=request.POST['reply']
#              music=request.POST['music_id']
#              comment=request.POST['comment_id']
#              user_data=request.POST['user_id']
#              music_data=Music.objects.get(id=music)
#              comment_data=Comment.objects.get(id=comment)
#              print(user_data)
#              user_data=User.objects.get(id=user_data)
#              reply=Reply(music_id=music_data,comment_id=comment_data,reply=reply,user_id=user,user_reply=user_data)
#              reply.save()
#              print('task is complete')
#              return redirect('play',id=music_data.id)

          





       # if request.method=='POST':
       #        music=Music.objects.get(id=id)
       #        print('user_id',request.user.id)
       #        if music.likes.filter(id=request.user.id).exists():
       #            print('work1')
       #            music.likes.remove(request.user)
       #        else:
       #               print('work2')
       #               music.likes.add(request.user)
       #        return redirect('play',id=music.id)



@login_required(login_url='/login/')
def play(request,id):
   if request.method=='GET':
          audio=Music.objects.filter(id=id)
          print(audio)
          comment=Comment.objects.filter(music_id__in=audio,reply=None).order_by('-id')

          no_of_comment=comment.count()
          return render(request,'music/play.html',{'audio':audio,'comment':comment,'count':no_of_comment})
   else:
          if request.POST.get("operation")=='like_submit' and request.is_ajax():
              user=request.user
              comment=request.POST.get('comment',None)
              print('comment',comment)
              music=request.POST['music_id']
              print('music',music)
              reply_id=request.POST.get('comment_id',None)
              print('reply_id',reply_id)
              audio=Music.objects.get(id=music)
              reply_data=None
              if reply_id:
                     reply_data=Comment.objects.get(id=reply_id)
              comment=Comment(user_id=user,music_id=audio,comment=comment,reply=reply_data)
              comment.save()
              return redirect('play',id=audio.id)





      



       
                  
                     
                     
                     

              

