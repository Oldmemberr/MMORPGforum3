from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, null=False)
    user = models.ManyToManyField(User, through = 'UsersSubscribed')


class Post(models.Model):
    TYPES = [
        ('TANKS', 'Танки'),
        ('HEALERS', 'Хилы'),
        ('DD', 'ДД'),
        ('MERCHANTS', 'Торговцы'),
        ('GUILDMASTERS', 'Гилдмастеры'),
        ('QUESTSGIVERS', 'Квестгиверы'),
        ('BLACKSMITHS', 'Кузнецы'),
        ('TANNERS', 'Кожевники'),
        ('POTIONMAKERS', 'Зельевары'),
        ('SPELLCASTERS', 'Мастера заклинаний'),
    ]
    avthor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avthor', default="")
    categoryType = models.CharField(default='', max_length=64, choices=TYPES)
    creationDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False)
    text = models.TextField()
    postImage = models.ImageField(upload_to='images/',default=None, null=True, blank=True)
    postFile = models.FileField(upload_to='file/', null=True, blank=True)
    category = models.ManyToManyField(Category,default='', max_length=64, through='PostCategory')

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class UsersSubscribed(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.user} is subscribed to category {self.category}'


class Comment(models.Model):
    userEditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='editor', default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commentText = models.TextField(null=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
     return 'Comment by {} on {}'.format(self.userEditor, self.post)


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comm')
    reply = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    # status = models.BooleanField()

    class Meta:
        unique_together = ('comment', 'reply')

    def __str__(self):
        return f'{self.reply} '

