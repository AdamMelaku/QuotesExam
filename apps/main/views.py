from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages



# Views that render pages.


def index(request):
    return render(request,'main/index.html')

def dashboard(request):

    context = {
    "user": User.objects.get(id=request.session["user_id"]),
    "quotes": Quote.objects.all(),
    "favorites":Favorite.objects.filter(user__id=request.session["user_id"]).distinct()
    }
    return render(request,'main/dashboard.html',context)

def user_info(request, id):
    context = {
    "user":User.objects.get(id=id),
    "posts":Quote.objects.all().filter(user=id)
    }
    return render(request,'main/userinfo.html',context)

#Views that process forms
def register(request):
    if User.objects.validate_user(request.POST):
        user = User.objects.create(
        name = request.POST.get("name"),
        alias = request.POST.get("alias"),
        date_of_birth = request.POST.get("date_of_birth"),
        email = request.POST.get("email"),
        password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
        )
        request.session["user_id"]=user.id
        return redirect("/dashboard")
    return redirect("/")

def login(request):
    if request.method == 'POST':
        login = User.objects.login_user(request.POST)
        if login:
            request.session["user_id"] = login[1].id
            return redirect ("/dashboard")
        else:
            messages.error(request,'Invalid credentials')
    return redirect("/")

def add_quote(request):
    if Quote.objects.validate_quote(request.POST):
        quote = Quote.objects.create(
        author = request.POST.get("author"),
        message = request.POST.get("message"),
        user = User.objects.get(id=request.session["user_id"])
        )
        return redirect ("/dashboard")
    else:
        messages.error(request,'Quoted by or Message is too short')
        return redirect ("/dashboard")

def favorites(request, id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Quote.objects.get(id=id)
    print "*"*50
    favorite = Favorite.objects.create(
    quote = quote,
    user = user
    )
    request.session["favs"]=favorite.quote.id
    return redirect ("/dashboard")

def remove(request, id):
    favorite=Favorite.objects.filter(id=id).first()
    favorite.delete()
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")
