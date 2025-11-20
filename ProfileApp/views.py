import base64
from django.shortcuts import render, redirect
from .forms import ProfileForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import Profile


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('profile_create')

    # 🔹 Encoder l'image en base64 pour l'affichage
    image_data = None
    if profile.image_blob:
        image_data = base64.b64encode(profile.image_blob).decode()

    return render(request, 'profile/profile_view.html', {
        'profile': profile,
        'image_data': image_data  # 🔹 Passer l'image encodée
    })


@login_required
def profile_create(request):
    try:
        if request.user.profile:
            return redirect('profile_view')
    except Profile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()  # 🔹 Le form s'occupe de l'image
            return redirect('profile_view')
    else:
        form = ProfileForm()

    return render(request, 'profile/profile_create.html', {'form': form})


@login_required
def profile_edit(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()  # 🔹 Le form s'occupe de l'image
            return redirect('profile_view')

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile/profile_edit.html', context)