from django.shortcuts import render , redirect
from django.conf import settings 
from django.db import models
from .form import MovieForm , LoginForm , AccountForm
from django.contrib.sessions.backends.cache import SessionStore as CacheSessionStore
from django.contrib.auth import authenticate
from .models import Accounts , WatchedMovie
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from  django.contrib import messages
import requests
import datetime as DT

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def  search_movie (request):
    messages = []
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user_name = request.session['user_name']
        watched_movie = WatchedMovie.objects.filter(user_id=request.session['user_id']).values()
        
        form = MovieForm()
        gte = DT.date.today() - DT.timedelta(days=7)
        gte = gte.strftime("%Y-%m-%d")
        lte = DT.date.today() + DT.timedelta(days=7)
        lte = lte.strftime("%Y-%m-%d")
        request_query = 'https://api.themoviedb.org/3/discover/movie?api_key=' + settings.TMDB_KEY + '&primary_release_date.gte='+gte +'&primary_release_date.lte='+lte
        
        req = requests.get(request_query)
        new_movie = req.json()['results']
        heading = "Latest Release and Comming Soon"
        if len(watched_movie) == 0:
            heading_2 = "Look like someone is busy!!!. "
        else:
            heading_2 = None
            
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            year = form.cleaned_data['year']
            request_query = 'https://api.themoviedb.org/3/search/movie?api_key=' + settings.TMDB_KEY + '&query=' + keyword
            current_year = DT.date.today().year
            if year is not None and year<=current_year and year>=1980:
                request_query = request_query + '&year='+ str(year)
            req = requests.get(request_query)
            json = req.json()
            json = json['results']
            result=[]
            for k in json:
                flag = False
                for i in watched_movie:
                        if k['id'] == i['movie_id']:
                                flag = True
                                break
                if flag:
                        continue
                else:
                        result.append(k)
            
            form = MovieForm()
            heading = "Here is Your Result!!"
            if len(result)==0:
                heading = "Oops.. Try some other keyword"
            return render (request, 'movie.html' , {'msg': heading ,'movie':result , 'form':form , 'user_name':user_name , 'watched_movie' : watched_movie ,'msg2':heading_2})
    result = []
    for k in new_movie:
                flag = False
                for i in watched_movie:
                        if k['id'] == i['movie_id']:
                                flag = True
                                break
                if flag:
                        continue
                else:
                        result.append(k)
    form = MovieForm()
    return render(request, 'movie.html' , {'msg': heading , 'movie':result , 'form': form , 'user_name' : user_name , 'watched_movie' : watched_movie , 'msg2':heading_2}   )
        
        

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

def startup (request):
    messages = []
    loginForm = LoginForm()
    registerForm = AccountForm()
    return render(request, 'index.html' , {'loginForm':loginForm, 'registerForm':registerForm})

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

def login (request):
    request.session.flush()
    form = LoginForm(request.POST)
    if form.is_valid():
        try:
            user = Accounts.objects.get(user_id=request.POST['user_id'])
        except ObjectDoesNotExist:
            messages.warning(request,'Wrong User Id or Password')
            return HttpResponseRedirect('/')
        if user is not None :
            passwrd = user.password
            if passwrd == request.POST['password']:
                request.session['user_name']  = user.Name
                request.session['user_id'] = user.user_id
                request.session.modified = True
                
                return redirect('movie.html')
    messages.warning(request,'Wrong User Id or Password')
    return HttpResponseRedirect('/')    

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

def register (request):
    form= AccountForm(request.POST)
    if form.is_valid():
        try:
            user = Accounts.objects.get(user_id=request.POST['user_id'])
        except ObjectDoesNotExist:
            user = None 
        if user is None :
            form.save()
            user = Accounts.objects.get(user_id=request.POST['user_id'])
            messages.success(request, 'Successfullly Register. Please Login.')
        else:
            messages.error(request, 'User Id Already Taken. Be Creative and Try Again. :P')
    else:
        messages.error(request, 'User Id Already Taken. Be Creative and Try Again. :P')       
    return HttpResponseRedirect('/')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------        

def logout (request):
    request.session.flush()
    return redirect('/')


#--------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_movie (request , MovieId):
    
    request_query = 'https://api.themoviedb.org/3/movie/'+MovieId+'?api_key=' + settings.TMDB_KEY
    req = requests.get(request_query)
    json = req.json()
    poster_path = json['poster_path']
    new_entry = WatchedMovie(user_id=request.session['user_id'],movie_id = MovieId,path=poster_path)
    new_entry.save()
    messages.success(request, 'Successfullly Added.')
    return HttpResponseRedirect('/movie.html')    

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

def remove_movie (request, MovieId):
    remove_entry = WatchedMovie.objects.filter(user_id=request.session['user_id'],movie_id = MovieId  )
    remove_entry.delete()
    messages.success(request, 'Successfullly Remove.')
    return HttpResponseRedirect('/movie.html')      
