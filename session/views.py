from django.shortcuts import render,redirect

from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash,get_user_model
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

UserModel = get_user_model()



def userlogin(request) :
    if request.method == 'POST':
        form = AuthenticationForm(request = request, data = request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username = username, password = password)
            
            if user is not None:
                login(request, user)
                return redirect('homeview')
            
            else :
                messages.error(request, 'username or password is invalid')
        else:
            messages.error(request, 'username or password is invalid')        
    else :
        form = AuthenticationForm()
    return render(request, 'session/login.html', {'form': form})        


def userlogout(request):
    logout(request)
    messages.success(request, 'Sucessfully logout')
    return redirect ('homeview')

from .forms import SignupForm

def registration(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user=form.save() 
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Active your account' 
            message = render_to_string('session/account.html',{
                'user' : user,
                'domain': current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                
            })    
            send_mail = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to = [send_mail])
            email.send()
            messages.success(request, 'Successfullly created')
            messages.info(request, 'Active your account accout from your mail you have provided')
            return redirect('login')
    else :
        form = SignupForm()
    
    return render(request, 'session/signup.html', {'form':form})
def activate(request,uidb64,token):
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated,you can now login')
        return redirect('login')
    else :
        messages.warning(request, 'activation link is invalid')
        return redirect('signup')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully')
            return redirect('homeview')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'session/change_password.html', {'form': form})

from .forms import UserProfileForm
from .models import UserProfile
   
def userProfile(request):
    try:
        instance = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        instance = None
        
    if request.method == "POST":
        if instance :
            form = UserProfileForm(request.POST, request.FILES, instance=instance)
        else :
            form = UserProfileForm(request.POST,request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'sucessfully saved your profile')   
            return redirect('homeview')
    else :
       
         form = UserProfileForm(instance=instance)
    context = {
         'form' : form
     }    
    return render(request, 'session/userproCreate.html',context)    

def ownerprofile(request):
    user = request.user
    return render(request, 'session/userprofile.html',{'user':user})
