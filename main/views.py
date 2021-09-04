from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from notes.models import Notes

User = get_user_model()


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.POST:
            data = request.POST['note']
            if data:
                new_note = Notes(note=data, user=request.user)
                new_note.save()
                messages.success(request, 'Note added!')
                return redirect('main:home')

        notes = Notes.objects.filter(user=request.user).all()
        if notes is None:
            notes = []
        return render(request, 'main/home.html', {'notes': notes})
    else:
        return redirect('main:login')


def login(request):
    if request.POST:
        data = request.POST
        email = data['email']
        password = data['password']

        if any(value == '' for value in data.values()):
            messages.error(request, 'You need to fill all the fields')
            return render(request, 'main/sign_up.html', {})

        if User.objects.filter(email=email).count() == 0:
            messages.error(request, 'Email doesn\'t exist')
            return redirect('main:login')

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main:home')
        else:
            messages.error(request, 'Password or email is incorrect')
            return redirect('main:login')
    return render(request, 'main/login.html', {})


def sign_up(request):
    if request.POST:
        data = request.POST
        email = data['email']
        password = data['password1']
        confirm_password = data['password2']

        if any(value == '' for value in data.values()):
            messages.error(request, 'You need to fill all the fields')
            return render(request, 'main/sign_up.html', {})

        if password != confirm_password:
            messages.error(request, 'You passwords aren\'t the same')
            return render(request, 'main/sign_up.html', {})

        if len(password) < 9:
            messages.error(request, 'You passwords need to be at least 9 characters long')
            return render(request, 'main/sign_up.html', {})

        new_user = User(email=email)
        new_user.set_password(password)
        new_user.save()

        messages.success(request, 'Account created!')
        return redirect('main:login')

    return render(request, 'main/sign_up.html', {})


def delete_note(request):
    data = request.POST['id']

    note = Notes.objects.filter(user=request.user, id=data).first()
    note.delete()

    messages.success(request, 'Note deleted successfully')
    return redirect('main:home')


def logout(request):
    logout(request)
    return redirect('main:login')
