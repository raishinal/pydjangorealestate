from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from accounts.forms import EditProfileForm
from django.contrib.auth import update_session_auth_hash



def register(request):
    if request.method == 'POST':
        # Get form values
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        password2= request.POST['password2']

        # check if password match
        if password == password2:
        #    check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    user= User.objects.create_user(username=username, password=password, email=email,
                     first_name=first_name, last_name= last_name)
                    #  login after register
                    # auth.login(request,user)
                    # messages.success(request, 'Your are now Logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'you are now registeref')
                    return redirect('login')

        else:
            messages.error(request,'Password did not match')
            return redirect('register')


    else:
        return render(request, 'accounts/register.html')

    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user= auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Your are now Logged In')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context= {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)

def editprofile(request):
    if request.method == 'POST':
        form= EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('editprofile')
        
    else:
        form= EditProfileForm(instance=request.user)
        args ={
            'form': form
        }
        return render(request,'accounts/editprofile.html', args)

def change_password(request):
    if request.method == 'POST':
        form= PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('editprofile')
        else:
            messages.error(request, 'Please enter correctly')
            return redirect('change-password')

    else:
        form= PasswordChangeForm(user=request.user)
        args ={
            'form': form
        }
        return render(request,'accounts/change_password.html', args)