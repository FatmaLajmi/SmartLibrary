# ProfileApp/views.py
from django.shortcuts import render, redirect
from .forms import ProfileForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile_view(request):
    # Vérifie si l'utilisateur a un profil
    try:
        profile = request.user.profile  # essaie de récupérer le profil lié
    except Profile.DoesNotExist:
        # Si pas de profil, redirige vers la page de création
        return redirect('profile_create')

    return render(request, 'profile_view.html', {'profile': profile})


@login_required
def profile_create(request):
    # Vérifie encore une fois si le profil existe
    try:
        if request.user.profile:
            return redirect('profile_view')
    except Profile.DoesNotExist:
        pass  # pas de profil → on continue

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # lie le profil à l'utilisateur
            profile.save()
            return redirect('profile_view')
    else:
        form = ProfileForm()

    return render(request, 'profile_create.html', {'form': form})
    return render(request, 'profile_view.html', {'profile': profile})


@login_required
def profile_edit(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_view')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'profile_edit.html', context)
