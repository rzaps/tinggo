from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, UserProfileForm, UserAvatarForm
from .models import User, UserProfile
from tinggo.supabase import create_user_profile, sign_up_user, sign_in_user, reset_password


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            
            # Get current language from session or default to 'en'
            current_language = request.session.get('django_language', 'en')
            
            supabase_user_data = {
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'role': form.cleaned_data.get('role'),
                'language': current_language,
            }
            
            supabase_user = sign_up_user(email, password, supabase_user_data)
            
            if supabase_user:
                user = form.save(commit=False)
                user.language = current_language  # Set language automatically
                user.save()
                UserProfile.objects.create(user=user)
                
                try:
                    user_data = {
                        'user_id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'role': user.role,
                        'country': user.country,
                        'city': user.city,
                        'language': user.language,
                        'created_at': user.created_at.isoformat(),
                    }
                    create_user_profile(user_data)
                except Exception as e:
                    print(f"Error creating user profile in Supabase: {e}")
                
                user = authenticate(email=user.email, password=password)
                login(request, user)
                messages.success(request, _('Welcome to TingGo! Your account has been created successfully.'))
                return redirect('home')
            else:
                messages.error(request, _('Failed to create account. Please try again.'))
                return render(request, 'accounts/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=profile)
        avatar_form = UserAvatarForm(request.POST, request.FILES, instance=user)
        
        if profile_form.is_valid() and avatar_form.is_valid():
            profile_form.save()
            avatar_form.save()
            
            try:
                user_data = {
                    'user_id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'country': user.country,
                    'city': user.city,
                    'language': user.language,
                    'updated_at': user.updated_at.isoformat(),
                }
                create_user_profile(user_data)
            except Exception as e:
                print(f"Error updating user in Supabase: {e}")
            
            messages.success(request, _('Profile updated successfully!'))
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile)
        avatar_form = UserAvatarForm(instance=user)
    
    context = {
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard(request):
    user = request.user
    
    if user.is_admin:
        return redirect('admin_dashboard')
    elif user.is_organizer:
        return redirect('organizer_dashboard')
    elif user.is_vendor:
        return redirect('vendor_dashboard')
    elif user.is_host:
        return redirect('host_dashboard')
    else:
        return redirect('participant_dashboard')


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            supabase_user = sign_in_user(email, password)
            
            if supabase_user:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, _('Welcome back!'))
                    return redirect('home')
                else:
                    messages.error(request, _('Invalid credentials.'))
            else:
                messages.error(request, _('Invalid credentials.'))
        else:
            messages.error(request, _('Please provide email and password.'))
    
    return render(request, 'accounts/custom_login.html')


def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            if reset_password(email):
                messages.success(request, _('Password reset email sent. Please check your inbox.'))
                return redirect('custom_login')
            else:
                messages.error(request, _('Failed to send password reset email. Please try again.'))
        else:
            messages.error(request, _('Please provide your email address.'))
    
    return render(request, 'accounts/custom_password_reset.html')


def custom_logout(request):
    logout(request)
    messages.success(request, _('You have been successfully logged out.'))
    return redirect('home')


@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, _('Access denied. Admin privileges required.'))
        return redirect('home')
    
    users = User.objects.all().order_by('-created_at')[:10]
    context = {
        'users': users,
        'total_users': User.objects.count(),
        'total_organizers': User.objects.filter(role=User.UserRole.ORGANIZER).count(),
        'total_participants': User.objects.filter(role=User.UserRole.PARTICIPANT).count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def organizer_dashboard(request):
    if not request.user.is_organizer:
        messages.error(request, _('Access denied. Organizer privileges required.'))
        return redirect('home')
    
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/organizer_dashboard.html', context)


@login_required
def participant_dashboard(request):
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/participant_dashboard.html', context)



    
    return redirect('/') 