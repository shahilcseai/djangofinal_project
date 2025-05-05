from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login
from .models import Camp, CampRegistration
from .forms import CampRegistrationForm, UserRegistrationForm, CampSearchForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Blood Donation Management System.')
            return redirect('camps:camp_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'camps/register_user.html', {'form': form})

def camp_list(request):
    form = CampSearchForm(request.GET)
    camps = Camp.objects.all().order_by('date')  # Show all camps, not just future ones
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if search:
            camps = camps.filter(
                Q(title__icontains=search) |
                Q(location__icontains=search) |
                Q(description__icontains=search)
            )
        
        if category:
            camps = camps.filter(category=category)
        
        if date_from:
            camps = camps.filter(date__date__gte=date_from)
        
        if date_to:
            camps = camps.filter(date__date__lte=date_to)

    # Group camps by status
    upcoming_camps = camps.filter(date__gte=timezone.now())
    past_camps = camps.filter(date__lt=timezone.now())

    context = {
        'upcoming_camps': upcoming_camps,
        'past_camps': past_camps,
        'form': form,
        'categories': Camp.CATEGORY_CHOICES,
    }
    return render(request, 'camps/camp_list.html', context)

def camp_detail(request, pk):
    camp = get_object_or_404(Camp, pk=pk)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = CampRegistration.objects.filter(camp=camp, user=request.user).exists()
    
    context = {
        'camp': camp,
        'is_registered': is_registered,
        'can_register': not camp.is_past and not camp.is_full and not is_registered,
    }
    return render(request, 'camps/camp_detail.html', context)

@login_required
def register_for_camp(request, pk):
    camp = get_object_or_404(Camp, pk=pk)
    
    if camp.is_past:
        messages.error(request, 'Cannot register for past camps.')
        return redirect('camps:camp_detail', pk=pk)
    
    if camp.is_full:
        messages.error(request, 'Camp is full.')
        return redirect('camps:camp_detail', pk=pk)
    
    if CampRegistration.objects.filter(camp=camp, user=request.user).exists():
        messages.error(request, 'You are already registered for this camp.')
        return redirect('camps:camp_detail', pk=pk)
    
    if request.method == 'POST':
        form = CampRegistrationForm(request.POST, camp=camp, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered for the camp! Check your email for confirmation.')
            return redirect('camps:camp_detail', pk=pk)
    else:
        form = CampRegistrationForm(camp=camp, user=request.user)
    
    return render(request, 'camps/register.html', {'form': form, 'camp': camp})

@login_required
def dashboard(request):
    user_registrations = CampRegistration.objects.filter(user=request.user).select_related('camp')
    upcoming_registrations = user_registrations.filter(camp__date__gte=timezone.now())
    past_registrations = user_registrations.filter(camp__date__lt=timezone.now())
    
    context = {
        'upcoming_registrations': upcoming_registrations,
        'past_registrations': past_registrations,
    }
    return render(request, 'camps/dashboard.html', context)
