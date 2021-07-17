from django.shortcuts import render
import csv
import os
from django.http import HttpResponse

from .models import books 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User,Click

from django.core import serializers
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
def ml(title_books):

###### helper functions. Use them when needed #######
    def get_title_from_index(index):
        return df[df.bookID == index]["title"].values[0]

    def get_index_from_title(title):
        return df[df.title == title]["bookID"].values[0]
##################################################

##Step 1: Read CSV File
    df = pd.read_csv("books.csv")

##Step 2: Select Features

    features = ['title','authors','publisher']
##Step 3: Create a column in DF which combines all selected features
    for feature in features:
        df[feature] = df[feature].fillna('')

    def combine_features(row):
        try:
            return row['title'] +" "+row['authors']+" "+row["publisher"]
        except:
            print("Error:", row )

    df["combined_features"] = df.apply(combine_features,axis=1)



##Step 4: Create count matrix from this new combined column
    cv = CountVectorizer()

    count_matrix = cv.fit_transform(df["combined_features"])
    

##Step 5: Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix) 

    movie_user_likes = title_books

## Step 6: Get index of this movie from its title
    movie_index = get_index_from_title(movie_user_likes)


    similar_movies =  list(enumerate(cosine_sim[movie_index]))


## Step 7: Get a list of similar movies in descending order of similarity score
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

    i=0

    ans=[]
    for element in sorted_similar_movies:
  

        ans.append([element[0]+1,get_title_from_index(element[0]+1)])
        i=i+1
        if i>9:
            break
    return ans
   

def index(request):

    return render(request, "register.html")
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            request.session['username'] = username
            request.session['password'] = password

            
            login(request, user)
            try:
                   query=Click.objects.get(user=user)
   
                   param=ml(query.last_click.title)

            except :
                   param=[]
            return render(request,"form.html",{"data":param})


          
           
        
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")
def logout_view(request):
    if request.session.has_key('username'):

       del request.session['username']

  
    logout(request)
    
    return render(request,"login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        try:
            yu=User.objects.filter(email=email)
        except:
            yu=None
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if username=="" or email=="" or password=="" or confirmation=="":
            return render(request, "register.html", {
                "message": "Please fill all the details!!"
            }) 
        else:          
            if yu:
               return render(request, "register.html", {
                "message": "Email already in use :("
               })
            else:
               if password != confirmation:
                  return render(request, "register.html", {
                "message": "Passwords must match."
                   })

        # Attempt to create new user
               try:
                  user = User.objects.create_user(username, email, password)
                  user.save()
               except IntegrityError:
                  return render(request, "your/register.html", {
                "message": "Username already taken."
                  })
               request.session['username'] = username
               request.session['password'] = password

               try:
                   query=Click.objects.get(user=user)
                   param=ml(query.last_click.title)

               except :
                   param=[]
               login(request, user)

               return render(request, "form.html",{"data":param})
              
        
        
    else:
        return render(request, "register.html")

def search(request):
        try:
            query=Click.objects.get(user=request.user)
   
            param=ml(query.last_click.title)

        except :
            param=[]
        return render(request,"form.html",{"data":param})
# Create your views here.
def add(request,id):
    return render(request,"summary.html",{"id":id})
def add_summary(request,id):
    
    a=books.objects.get(bookID=id)
    a.summary=request.POST["summary"]
    a.save()
    return HttpResponseRedirect(reverse("details",kwargs={'id':id}))



def book_csv(request):
    # Import CSV
    data = pd.read_csv ('books.csv')   

    df = pd.DataFrame(data, columns= ['bookID','title','authors','publisher','average_rating','summary'])




# Insert DataFrame to Table
    for row in df.itertuples():
        a=books()
        a.bookID=row[1]
        a.publisher=row[4]
        a.title=row[2]
        a.author=row[3]
        a.average_ratting=row[5]
        a.summary=row[6]
        a.save()
    return HttpResponse("success")

def list_books(request):
    title_book=request.POST['book_name']
    a=books.objects.filter(title__icontains=title_book)

    ans=ml(a[0].title)



    return render(request,"main.html",{"data":ans,"current_book":a})
def details(request,id):
    title_book=id
    a=books.objects.get(bookID=title_book)
    try:
        b=Click.objects.get(user=request.user)

        b.user=request.user

        b.last_click=a
        b.save()
    except :
        b=Click()
        b.user=request.user

        b.last_click=a
        b.save()
    ans=ml(a.title)
 


    return render(request,"view.html",{"details":ans,"current_book":a})   
   
