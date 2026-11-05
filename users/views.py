from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
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
        location = request.POST.get('location', '')

        if username and password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password,
                    gender=gender,
                    location=location
                )
                user.save()
                login(request, user)  # Auto-login user after sign-up
                return redirect('discover')
            else:
                return render(request, 'register.html', {'error': 'Username already taken.'})

    # Pre-fill location/gender if passed from home page search box
    initial_gender = request.GET.get('gender', '')
    initial_location = request.GET.get('location', '')
    
    return render(request, 'register.html', {
        'initial_gender': initial_gender, 
        'initial_location': initial_location
    })

def logout_view(request):
    logout(request)
    return redirect('home')

def discover_view(request):
    query = request.GET.get('q', '')
    gender_filter = request.GET.get('gender', '')
    
    profiles = User.objects.all()
    
    # Exclude currently logged in user from search results
    if request.user.is_authenticated:
        profiles = profiles.exclude(id=request.user.id)
        
    if gender_filter:
        profiles = profiles.filter(gender__iexact=gender_filter)

    if query:
        profiles = profiles.filter(
            Q(username__icontains=query) | 
            Q(location__icontains=query) | 
            Q(gender__icontains=query)
        )
        
    return render(request, 'discover.html', {'profiles': profiles, 'query': query})