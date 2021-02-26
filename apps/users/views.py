from django.shortcuts import render, get_object_or_404
from django.views import View

from apps.blog.models import Publication
from apps.users.models import AuthorProfile
from apps.users.forms import CustomUserChangeForm


class UserDashboardView(View):

    def get(self, request):
        user = get_object_or_404(AuthorProfile, pk=request.user.pk)
        return render(request, 'users/dashboard.html', {'user': user})


class UserProfileView(View):

    def get(self, request):
        user = get_object_or_404(AuthorProfile, pk=request.user.pk)
        form = CustomUserChangeForm(instance=user)
        return render(request, 'users/profile.html', {'user': user, 'form': form})

    def post(self, request):
        user = get_object_or_404(AuthorProfile, pk=request.user.pk)
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save(commit=True)
        else:
            form = CustomUserChangeForm()
        return render(request, 'users/profile.html', {'user': user, 'form': form})


class UsersList(View):

    def get(self, request):
        users = AuthorProfile.objects.all()
        context = {'users': users}

        return render(request, 'users/users_list.html', context=context)


class UserCard(View):

    def get(self, request, pk):
        user = get_object_or_404(AuthorProfile, pk=pk)
        publication = Publication.objects.filter(author=user)
        context = {'user': user, 'publication': publication}
        return render(request, 'users/user_card.html', context=context)
