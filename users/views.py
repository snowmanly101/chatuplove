from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q

User = get_user_model()

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender', 'female')
        looking_for = request.POST.get('looking_for', 'male')
        location = request.POST.get('location', '')
        height = request.POST.get('height', '')
        body_type = request.POST.get('body_type', '')
        marital_status = request.POST.get('marital_status', 'single')
        occupation = request.POST.get('occupation', '')
        bio = request.POST.get('bio', '')

        if username and password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password,
                    gender=gender,
                    looking_for=looking_for,
                    location=location,
                    height=height,
                    body_type=body_type,
                    marital_status=marital_status,
                    occupation=occupation,
                    bio=bio
                )
                user.save()
                login(request, user)
                return redirect('profile')
            else:
                return render(request, 'register.html', {'error': 'Username already taken.'})

    initial_gender = request.GET.get('gender', '')
    initial_location = request.GET.get('location', '')
    
    return render(request, 'register.html', {
        'initial_gender': initial_gender, 
        'initial_location': initial_location
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def free_dating_view(request):
    return render(request, 'users/free_dating.html')

def dating_advice_view(request):
    return render(request, 'users/dating_advice.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.bio = request.POST.get('bio', request.user.bio)
        request.user.occupation = request.POST.get('occupation', request.user.occupation)
        request.user.location = request.POST.get('location', request.user.location)
        request.user.height = request.POST.get('height', request.user.height)
        request.user.body_type = request.POST.get('body_type', request.user.body_type)
        if 'profile_picture' in request.FILES:
            request.user.profile_picture = request.FILES['profile_picture']
        request.user.save()
        return redirect('profile')
        
    return render(request, 'users/profile.html')

def discover_view(request):
    query = request.GET.get('q', '')
    gender_filter = request.GET.get('gender', '')
    location_filter = request.GET.get('location', '')
    
    profiles = User.objects.all()
    
    if request.user.is_authenticated:
        profiles = profiles.exclude(id=request.user.id)
        
    if gender_filter:
        profiles = profiles.filter(gender__iexact=gender_filter)

    if location_filter:
        profiles = profiles.filter(location__icontains=location_filter)

    if query:
        profiles = profiles.filter(
            Q(username__icontains=query) | 
            Q(location__icontains=query) | 
            Q(bio__icontains=query) |
            Q(occupation__icontains=query)
        )
        
    return render(request, 'discover.html', {'profiles': profiles, 'query': query})