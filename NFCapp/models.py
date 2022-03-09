from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from embed_video.fields import EmbedVideoField


class Banners(models.Model) :
    img = models.ImageField(upload_to="banners/")
    alt_text = models.CharField(max_length=150)

    class Meta :
        verbose_name_plural = 'Banners'

    def __str__(self) :
        return self.alt_text

    def image_tag(self) :
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))


class Services(models.Model) :
    title = models.CharField(max_length=150)
    detail = models.TextField()
    img = models.ImageField(upload_to="services/", null=True)

    def __str__(self) :
        return self.title

    def image_tag(self) :
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))


class Page(models.Model) :
    title = models.CharField(max_length=200)
    detail = models.TextField()

    def __str__(self) :
        return self.title


class Enquiry(models.Model) :
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    detail = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.full_name


class Gallery(models.Model) :
    title = models.CharField(max_length=150)
    detail = models.TextField()
    img = models.ImageField(upload_to="gallery/", null=True)

    def __str__(self) :
        return self.title

    def image_tag(self) :
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))


class GalleryImage(models.Model) :
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)
    alt_text = models.CharField(max_length=150)
    img = models.ImageField(upload_to="gallery_imgs/", null=True)

    def __str__(self) :
        return self.alt_text

    def image_tag(self) :
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))


class Subscriber(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=20)
    adress = models.TextField()
    img = models.ImageField(upload_to="subs/", null=True)

    def __str__(self) :
        return str(self.user)

    def image_tag(self) :
        if self.img :
            return mark_safe('<img src="%s" width="80" />' % (self.img.url))
        else :
            return "no_imge"


@receiver(post_save, sender=User)
def create_subscriber(sender, instance, created, **kwrags) :
    if created :
        Subscriber.objects.create(user=instance)


class Trainer(models.Model) :
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=100)
    address = models.TextField()
    is_active = models.BooleanField(default=False)
    detail = models.TextField()
    img = models.ImageField(upload_to="trainers/")

    facebook = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    pinterest = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) :
        return str(self.full_name)

    def image_tag(self) :
        if self.img :
            return mark_safe('<img src="%s" width="80" />' % (self.img.url))
        else :
            return 'no-image'


class Notify(models.Model) :
    notify_detail = models.TextField()
    read_by_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    read_by_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) :
        return str(self.notify_detail)


class NotifUserStatus(models.Model) :
    notif = models.ForeignKey(Notify, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)


class TrainerAchivement(models.Model) :
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    detail = models.TextField()
    img = models.ImageField(upload_to="trainers_achivements/")

    def __str__(self) :
        return str(self.title)

    def image_tag(self) :
        if self.img :
            return mark_safe('<img src="%s" width="80" />' % (self.img.url))
        else :
            return 'no-image'


class TrainerNotification(models.Model) :
    notif_msg = models.TextField()

    def __str__(self) :
        return str(self.notif_msg)

    def save(self, *args, **kwargs) :
        super(TrainerNotification, self).save(*args, **kwargs)
        channel_layer = get_channel_layer()
        notif = self.notif_msg
        total = TrainerNotification.objects.all().count()
        async_to_sync(channel_layer.group_send)(
            'noti_group_name', {
                'type' :'send_notification',
                'value' :json.dumps({'notif' :notif, 'total' :total})
            }
        )


class NotifTrainerStatus(models.Model) :
    notif = models.ForeignKey(TrainerNotification, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta :
        verbose_name_plural = 'Trainer Notification Status'


class TrainerMsg(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True)
    message = models.TextField()

    class Meta :
        verbose_name_plural = 'Messages For Trainer'


class TrainerSubscriberReport(models.Model) :
    report_for_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True,
                                           related_name='report_for_trainer')
    report_for_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='report_for_user')
    report_from_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True,
                                            related_name='report_from_trainer', blank=True)
    report_from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='report_from_user',
                                         blank=True)
    report_msg = models.TextField()


class YouTube(models.Model) :
    video = EmbedVideoField()

    class Meta :
        verbose_name_plural = 'YouTube'