from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from apps.blog.models import Publication


@receiver(post_save, sender=Publication)
def new_publication_notification(sender, **kwargs):
    instance = kwargs['instance']

    if not kwargs['created']:
        return

    publication_url = f'{settings.HOST}/admin/blog/publication/{instance.id}/change/'
    send_mail(
        'Новая публикация',
        f'Публикация нуждается в модерации - {publication_url}',
        settings.EMAIL_HOST_USER,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )


@receiver(post_save, sender=Publication)
def reject_publication_notification(sender, **kwargs):
    instance = kwargs['instance']

    if not kwargs['created'] and instance.status == Publication.STATUS.DECLINED and not instance.rejection_sent:
        send_mail(
            'Ваша публикация не прошла модерацию',
            f'Причина отклонения - {instance.rejection_reason}',
            settings.EMAIL_HOST_USER,
            [instance.author.email],
            fail_silently=False,
        )
        instance.rejection_sent = True
        instance.save()
