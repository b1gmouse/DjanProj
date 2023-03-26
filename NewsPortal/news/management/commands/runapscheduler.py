import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.tasks import new_post_subscription

from news.models import Post, PostCategory

logger = logging.getLogger(__name__)


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

    msg.attach_alternative(html, 'text/html')
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        @receiver(m2m_changed, sender=PostCategory)
        def notify_subscribers(sender, instance, **kwargs):
            scheduler.add_job(
                new_post_subscription(instance),
                trigger=CronTrigger(second="*/5"),
              #trigger=CronTrigger(
                #day_of_week="fri", hour="18", minute="00"
             #),
                id="my_job",  # The `id` assigned to each job MUST be unique
                max_instances=1,
                replace_existing=True,
            )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
