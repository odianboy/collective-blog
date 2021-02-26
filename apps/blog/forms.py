from django import forms
from apps.blog.models import Publication, CommentPublication, PublicationRating, Category


class PublicationForm(forms.ModelForm):
    category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(), required=False)

    class Meta:
        model = Publication
        fields = ('title', 'short_description', 'text', 'category')


class DeletePublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = []


class CommentPublicationForm(forms.ModelForm):

    class Meta:
        model = CommentPublication
        fields = ('text', )


class PublicationRatingForm(forms.ModelForm):

    class Meta:
        model = PublicationRating
        fields = ('rating', )
