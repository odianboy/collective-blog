from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Q
from django.utils import timezone

from apps.users.models import AuthorProfile
from apps.blog.models import Publication, Category, PublicationRating
from apps.blog.forms import CommentPublicationForm, PublicationRatingForm, PublicationForm, DeletePublicationForm


class Index(View):

    def get(self, request):
        search_query = request.GET.get('search', '')

        query = Publication.objects.filter(status=Publication.STATUS.APPROVED)
        if search_query:
            query = query.filter(
                Q(title__icontains=search_query) | Q(short_description__icontains=search_query)
            )

        by_date = request.GET.get('by_date', '')
        if by_date and by_date == 'oldest':
            query = query.order_by('publication_date')
        else:
            query = query.order_by('-publication_date')

        by_author = request.GET.get('by_author', '')
        try:
            by_author = int(by_author)
        except ValueError:
            pass

        if by_author and isinstance(by_author, int):
            query = query.filter(author_id=by_author)

        context = {
            'posts': query,
            'categories': Category.objects.all(),
            'authors': AuthorProfile.objects.filter(publications__isnull=False).distinct()
        }
        return render(request, 'blog/index.html', context=context)


class CategoryPosts(View):

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        posts = Publication.objects.filter(category__name=category)

        return render(request, 'post/post_category.html', context={'category': category, 'posts': posts})


class UserPublicationView(View):

    def get(self, request):
        user = get_object_or_404(AuthorProfile, pk=request.user.pk)
        publication = Publication.objects.filter(author=user)
        return render(request, 'post/post_user.html', {'publication':  publication, 'user': user})


class UserPublicationDetailView(View):

    def get(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        comments = publication.comments.filter(active=True)
        comment_form = CommentPublicationForm(instance=publication)
        rating = publication.get_rating()
        rating_form = PublicationRatingForm()

        rating_exist = True
        if publication.author != request.user:
            rating_exist = PublicationRating.objects.filter(user=request.user, publication=publication).exists()

        context = {
            'publication': publication,
            'comments': comments,
            'comment_form': comment_form,
            'rating_form': rating_form,
            'rating': rating,
            'rating_exist': rating_exist
        }
        return render(request, 'post/post_user_detail.html', context=context)

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        comments = publication.comments.filter(active=True)
        comment_form = CommentPublicationForm(data=request.POST)
        rating_form = PublicationRatingForm(data=request.POST)
        if rating_form.is_valid():
            new_rating = rating_form.save(commit=False)
            new_rating.publication = publication
            new_rating.user = request.user
            new_rating.save()
            publication.save()
        else:
            rating_form = PublicationRatingForm()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.publication = publication
            new_comment.author = request.user
            new_comment.save()

        else:
            comment_form = CommentPublicationForm()

        rating_exist = True
        if publication.author != request.user:
            rating_exist = PublicationRating.objects.filter(user=request.user, publication=publication).exists()

        context = {
            'publication': publication,
            'comments': comments,
            'comment_form': comment_form,
            'rating_form': rating_form,
            'rating': publication.get_rating(),
            'rating_exist': rating_exist
        }
        return render(request, 'post/post_user_detail.html', context=context)


class UserPostEdit(View):

    def get(self, request, pk):
        post = get_object_or_404(Publication, pk=pk)
        form = PublicationForm(instance=post)
        return render(request, 'post/post_user_edit.html', {'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Publication, pk=pk)
        form = PublicationForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publication_date = timezone.now()
            post.save()
            return redirect('post_user_detail', pk=post.pk)
        else:
            form = PublicationForm(instance=post)
        return render(request, 'post/post_user_edit.html', {'form': form})


class UserPostDelete(View):

    def get(self, request, pk):
        post = get_object_or_404(Publication, pk=pk)
        form = DeletePublicationForm(instance=post)
        return render(request, 'post/post_user_delete.html', {'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Publication, id=pk)

        if request.method == 'POST':
            form = DeletePublicationForm(request.POST, instance=post)

            if form.is_valid():
                post.delete()
                return redirect('/')

        else:
            form = DeletePublicationForm(instance=post)

        return render(request, 'post/post_user_delete.html', context={'form': form})


class UserPostNew(View):

    def get(self, request):
        return render(request, 'post/post_user_new.html', context={'new_post_form': PublicationForm()})

    def post(self, request):
        new_post_form = PublicationForm(request.POST, request.FILES)
        if new_post_form.is_valid():
            post = new_post_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_user_detail', pk=post.pk)
        else:
            new_post_form = PublicationForm()
        return render(request, 'post/post_user_new.html', context={'new_post_form': new_post_form})
