from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'id' in request.session:
        return redirect("/dashboard")
    return render(request,"dash_app/index.html")

def create(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hash1)


    request.session['id'] = user.id
    request.session['first_name'] = user.first_name


    return redirect("/dashboard")

def create_admin(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hash1)

    return redirect("/dashboard")

def login(request):
    errors = User.objects.login_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)

        return redirect("/")

    user = User.objects.get(email=request.POST['email'])
    request.session['id'] = user.id
    request.session['first_name'] = user.first_name
    request.session['level'] = user.user_level



    return redirect("/dashboard")

def delete_message(request,id):
    message = Message.objects.get(id=id)
    message.delete()

    return redirect("/users/show/{}".format(id))

def delete_comment(request,id, user_id):
    comment = Comment.objects.get(id=id)
    comment.delete()

    return redirect("/users/show/{}".format(user_id))

def update_user(request, id):
    user = User.objects.get(id=id)
    user.email = request.POST['email']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.user_level = request.POST['user_level']
    user.save()

    return redirect("/users/show/{}".format(id))

def update_password(request, id):
    user = User.objects.get(id=id)
    hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    user.password = hash1
    user.save()

    return redirect("/users/show/{}".format(id)) 


def remove_user(request,id):
    user = User.objects.get(id=id)
    user.delete()

    return redirect("/dashboard/admin")

def edit_profile(request):
    user = User.objects.get(id=request.session['id'])

    context = {
        'user':user
    }

    return render(request, "dash_app/edit_profile.html",context)

def edit_admin(request,id):
    user = User.objects.get(id=id)

    context = {
        'user': user
    }

    return render(request, "dash_app/edit_admin.html", context)

def show_user(request,id):
    user = User.objects.get(id=id)

    context = {
        'user': user
    }

    return render(request, "dash_app/user_page.html", context)

def dashboard(request):
    context = {
        'users' : User.objects.all(),
        'admin' : True
    }

    return render(request,"dash_app/dashboard.html",context)

def dashboard_admin(request):
    context = {
        'users' : User.objects.all(),
        'admin' : False
    }

    return render(request,"dash_app/dashboard.html", context)

def new_user(request):
    return render(request,"dash_app/add_user.html")

def post_message(request):
    poster = User.objects.get(id=request.session['id'])
    recipient = User.objects.get(id=request.POST['user_id'])

    message = Message.objects.create(message=request.POST['message'],poster = poster, recipient=recipient)

    return redirect("/users/show/{}".format(request.POST['user_id']))



def post_comment(request):
    message = Message.objects.get(id=request.POST['message_id'])
    user = User.objects.get(id=request.session['id'])

    comment = Comment.objects.create(comment=request.POST['comment'], user= user, message = message)

    return redirect("/users/show/{}".format(request.POST['user_id']))

def login_page(request):
    return render(request,"dash_app/login.html")

def register_page(request):
    return render(request,"dash_app/register.html")

def logout(request):
    request.session.flush()

    return redirect("/")
