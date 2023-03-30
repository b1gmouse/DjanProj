from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory


news_list = []


def get_subscriber(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email


def new_post_subscription(instance):
    template = 'new_post.html'

    for category in instance.category.all():
        email_subject = f'New post in category: "{category}"'
        user_emails = get_subscriber(category)

        html = render_to_string(
            template_name=template,
            context={
                'category': category,
                'post': instance,
            },
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_emails,
        )
        news_list[len(news_list)+1] = instance

    msg.attach_alternative(html, 'text/html')
    msg.send()


@shared_task()
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_subscription(instance)


@shared_task()
def get_news():
    print('Your news on this week: ')
    a = len(news_list)
    for i in range(0, a):
        print(new_post_subscription(news_list[i]))


@shared_task()
def clear_old():
    news_list.clear()

