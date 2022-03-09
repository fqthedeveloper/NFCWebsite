from django.contrib import admin
from . import models

from embed_video.admin import AdminVideoMixin
from .models import YouTube


class BannersAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image_tag')


admin.site.register(models.Banners, BannersAdmin)


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')


admin.site.register(models.Services, ServicesAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(models.Page, PageAdmin)


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'detail', 'send_time')


admin.site.register(models.Enquiry, EnquiryAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')


admin.site.register(models.Gallery, GalleryAdmin)


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image_tag')


admin.site.register(models.GalleryImage, GalleryImageAdmin)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_tag', 'mobile')


admin.site.register(models.Subscriber, SubscriberAdmin)


class TrainerAdmin(admin.ModelAdmin) :
    list_editable = ('is_active',)
    list_display = ('full_name', 'is_active', 'image_tag', 'detail')


admin.site.register(models.Trainer, TrainerAdmin)


class NotifyAdmin(admin.ModelAdmin) :
    list_display = ('notify_detail', 'read_by_user', 'read_by_trainer')


admin.site.register(models.Notify, NotifyAdmin)


class NotifUserStatusAdmin(admin.ModelAdmin) :
    list_display = ('notif', 'user', 'status')


admin.site.register(models.NotifUserStatus, NotifUserStatusAdmin)


class TrainerAchivementAdmin(admin.ModelAdmin) :
    list_display = ('title', 'image_tag')


admin.site.register(models.TrainerAchivement, TrainerAchivementAdmin)


class TrainerNotificationAdmin(admin.ModelAdmin) :
    list_display = ('notif_msg',)


admin.site.register(models.TrainerNotification, TrainerNotificationAdmin)


class TrainerNotificationStatusAdmin(admin.ModelAdmin) :
    list_display = ('notif',)


admin.site.register(models.NotifTrainerStatus, TrainerNotificationStatusAdmin)


# SubscriberMsg
class TrainerMsgAdmin(admin.ModelAdmin) :
    list_display = ('user', 'trainer', 'message')


admin.site.register(models.TrainerMsg, TrainerMsgAdmin)


# Report For user
class TrainerSubscriberReportAdmin(admin.ModelAdmin) :
    list_display = ('report_msg', 'report_for_trainer', 'report_for_user', 'report_from_trainer', 'report_from_user')


admin.site.register(models.TrainerSubscriberReport, TrainerSubscriberReportAdmin)


class YouTubeAdmin(AdminVideoMixin, admin.ModelAdmin) :
    pass


admin.site.register(YouTube, YouTubeAdmin)


