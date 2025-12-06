from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import Position, Vote
from .forms import LoginForm

def index(request):
    return render(request, 'base/index.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('voting_dashboard')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('voting_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    context = {
        'form': form,
    }
    return render(request, 'base/login.html', context)


@login_required(login_url='login')
def voting_dashboard(request):
    if request.user.has_voted:
        return redirect('voting_success')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                positions = Position.objects.all()
                for position in positions:
                    candidate_id = request.POST.get(f'position_{position.id}')
                    
                    if candidate_id:
                        Vote.objects.create(
                            user=request.user,
                            position=position,
                            candidate_id=candidate_id
                        )
                request.user.has_voted = True
                request.user.save()
                
            return redirect('voting_success')
            
        except Exception as e:
            return render(request, 'base/vote.html', {'error': str(e)})

    context = {
        'positions': Position.objects.prefetch_related('candidates').all()
    }
    return render(request, 'base/vote.html', context)

@login_required(login_url='login')
def voting_success(request):
    user_votes = Vote.objects.filter(user=request.user).select_related('candidate', 'position').order_by('position__name')
    
    context = {
        'user_votes': user_votes,
        'submission_date': user_votes.first().timestamp if user_votes.exists() else None,
    }
    return render(request, 'base/success.html', context)