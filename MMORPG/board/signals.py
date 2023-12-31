from .models import Comment
from datetime import date
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Post, UsersSubscribed,Category
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.models import Site
from .management.commands.runapscheduler import weekly_mail


@receiver(post_save, sender=Post)
def mail_to_subscribers(sender, instance, created, **kwargs):
    try:
        post = instance
        category = post.category.get().id
        header = post.header
        main_text = post.main_text[:50]
        current_site = Site.objects.get_current()
        post_link = f"http://{current_site.name}{reverse('details', args=(post.id,))}"
        subscribers_list = UsersSubscribed.objects.filter(category=category)
        for each in subscribers_list:
            hello_text = f'Здравствуй, {User}. Новая статья в твоём любимом разделе!\n'
            html_content = render_to_string('account/email/mail_to_subscribers.html', {'header': header, 'main_text': main_text, 'hello_text': hello_text, 'post_link': post_link})
            msg = EmailMultiAlternatives(
            subject=f'{header}',
            body=hello_text+main_text,
            from_email='glavpochta87@gmail.com',
            to=[each.user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    except ObjectDoesNotExist:
        pass

@receiver(weekly_mail)
def weekly_mail(sender, **kwargs):
    categories = Category.objects.all()
    current_site = Site.objects.get_current()
    site_link = f"http://{current_site.name}"
    for category in categories:
        subscribers_list = UsersSubscribed.objects.filter(category=category)
        posts = Post.objects.filter(category=category).filter(creation_date_time__week=date.today().isocalendar()[1]-1)
        if posts.count()>0:
            for each in subscribers_list:
                hello_text = f'Здравствуй, {User}. Подборка статей за неделю в твоём любимом разделе {category}!\n'
                header = 'Подборка статей за неделю'
                html_content = render_to_string('account/email/weekly_mail.html',
                                                {'header': header, 'hello_text': hello_text, 'posts': posts, 'category': category, 'site_link': site_link})
                msg = EmailMultiAlternatives(
                subject=f'{header}',
                body=hello_text,
                from_email='glavpochta87@gmail.com',
                to=[each.user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()


@receiver(post_save, sender=Comment)
def send_mail(sender, instance, created, **kwargs):

    if created:
        user = instance.post.userEditor

        html = render_to_string(
            'accounts/Mail.html',
            {
                'user': user,
                'comment': instance,
             },
        )

        msg = EmailMultiAlternatives(
                subject=f'Новый коммент',
                from_email='glavpochta87@gmail.com',
                to=[user.email]
            )

        msg.attach_alternative(html, 'text/html')
        msg.send()
    else:
        user = instance.avthor

        html = render_to_string(
            'accounts/Mail.html',
            {
                'user': user,
                'comment': instance,
             },
        )

        msg = EmailMultiAlternatives(
                subject=f'Ответ',
                from_email='glavpochta87@gmail.com',
                to=[user.email]
                # recipient_lst={instance.post.userEditor.email}
            )

        msg.attach_alternative(html, 'text/html')
        msg.send()