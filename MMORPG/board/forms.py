from django import forms
from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        #fields = '__all__'
        fields = ['title', 'text','avthor','categoryType','postImage',"category"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'categoryType': forms.Select(choices=Post.TYPES, attrs={'class': 'form-select'}),
            'image': forms.FileInput(),
            'category': forms.Textarea(attrs={'class': 'form-control'}),

            }

        labels = {
                'title': 'Заголовок ',
                'text': 'Объявление',
                'categoryType': 'Категория',
                'postImage': 'Изображение',
                'category':'Категория ещё'
            }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['userEditor', 'commentText']
        widgets = {
            'commentText': forms.Textarea(attrs={'class': 'form-control'}),
            'userEditor': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'commentText': 'Комментарий',
            'userEditor': 'Имя',
        }


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentText', 'userEditor']
