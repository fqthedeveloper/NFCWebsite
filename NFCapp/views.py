from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import JsonResponse
from .models import YouTube
from . import models
from . import forms


def home(request) :
    banners = models.Banners.objects.all()
    services = models.Services.objects.all()
    gimgs = models.GalleryImage.objects.all().order_by('-id')
    return render(request, 'home.html', {'banners' :banners, 'services' :services, 'gimgs' :gimgs})


def page_detail(request, id) :
    page = models.Page.objects.get(id=id)
    return render(request, 'page.html', {'page' :page})


def enquiry(request) :
    msg = ''
    if request.method == 'POST' :
        form = forms.EnquiryForm(request.POST)
        if form.is_valid() :
            form.save()
            msg = 'Data Has Been Saved'
    form = forms.EnquiryForm
    return render(request, 'enquiry.html', {'form' :form, 'msg' :msg})


def gallery(request) :
    gallery = models.Gallery.objects.all().order_by('-id')
    return render(request, 'gallery.html', {'gallerys' :gallery})


def gallery_detail(request, id) :
    gallery = models.Gallery.objects.get(id=id)
    gallery_imgs = models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    return render(request, 'gallery_imgs.html', {'gallery_imgs' :gallery_imgs, 'gallery' :gallery})


def signup(request) :
    msg = None
    if request.method == 'POST' :
        form = forms.SignUp(request.POST)
        if form.is_valid() :
            form.save()
            msg = 'Thank you for register.'
    form = forms.SignUp
    return render(request, 'registration/signup.html', {'form' :form, 'msg' :msg})


def user_dashboard(request) :
    # Notification
    data = models.Notify.objects.all().order_by('-id')
    notifStatus = False
    totalUnread = 0
    for d in data :
        try :
            notifStatusData = models.NotifUserStatus.objects.get(user=request.user, notif=d)
            if notifStatusData :
                notifStatus = True
        except models.NotifUserStatus.DoesNotExist :
            notifStatus = False
        if not notifStatus :
            totalUnread = totalUnread + 1

    return render(request, 'user/dashboard.html')


def update_profile(request) :
    msg = None
    if request.method == 'POST' :
        form = forms.ProfileForm(request.POST, instance=request.user)
        if form.is_valid() :
            form.save()
            msg = 'Data has been saved'
    form = forms.ProfileForm(instance=request.user)
    return render(request, 'user/update-profile.html', {'form' :form, 'msg' :msg})


def trainerlogin(request) :
    msg = ''
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        trainer = models.Trainer.objects.filter(username=username, password=password).count()
        if trainer > 0 :
            request.session['trainerLogin'] = True
            return redirect('/trainer_dashboard')
        else :
            msg = 'Invalid!!'
    form = forms.TrainerLoginForm
    return render(request, 'trainer/login.html', {'form' :form, 'msg' :msg})


def trainerlogout(request) :
    del request.session['trainerLogin']
    return redirect('/trainerlogin')


def trainer_dashboard(request) :
    return render(request, 'trainer/dashboard.html')


def trainer_profile(request) :
    trainer = models.Trainer.objects.get()
    msg = None
    if request.method == 'POST' :
        form = forms.TrainerProfileForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid() :
            form.save()
            msg = 'Profile has been updated'
    form = forms.TrainerProfileForm(instance=trainer)
    return render(request, 'trainer/profile.html', {'form' :form, 'msg' :msg})


def notifs(request) :
    data = models.Notify.objects.all().order_by('-id')
    return render(request, 'notifs.html')


# Get All Notifications
def get_notifs(request) :
    data = models.Notify.objects.all().order_by('-id')
    notifStatus = False
    jsonData = []
    totalUnread = 0
    for d in data :
        try :
            notifStatusData = models.NotifUserStatus.objects.get(user=request.user, notif=d)
            if notifStatusData :
                notifStatus = True
        except models.NotifUserStatus.DoesNotExist :
            notifStatus = False
        if not notifStatus :
            totalUnread = totalUnread + 1
        jsonData.append({
            'pk' :d.id,
            'notify_detail' :d.notify_detail,
            'notifStatus' :notifStatus
        })
    # jsonData=serializers.serialize('json', data)
    return JsonResponse({'data' :jsonData, 'totalUnread' :totalUnread})


# Mark Read By user
def mark_read_notif(request) :
    notif = request.GET['notif']
    notif = models.Notify.objects.get(pk=notif)
    user = request.user
    models.NotifUserStatus.objects.create(notif=notif, user=user, status=True)
    return JsonResponse({'bool' :True})


def trainer_subscribers(request) :
    return render(request, 'trainer/trainer_subscribers.html')


def trainer_changepassword(request) :
    msg = None
    if request.method == 'POST' :
        new_password = request.POST['new_password']
        updateRes = models.Trainer.objects.filter(pk=request.session['trainerid']).update(pwd=new_password)
        if updateRes :
            del request.session['trainerLogin']
            return redirect('/trainerlogin')
        else :
            msg = 'Something is wrong!!'
    form = forms.TrainerChangePassword
    return render(request, 'trainer/trainer_changepassword.html', {'form' :form})


# Trainer Notifications
def trainer_notifs(request) :
    data = models.TrainerNotification.objects.all()
    trainer = models.Trainer.objects.get()
    jsonData = []
    totalUnread = 0
    for d in data :
        try :
            notifStatusData = models.NotifTrainerStatus.objects.get(trainer=trainer, notif=d)
            if notifStatusData :
                notifStatus = True
        except models.NotifTrainerStatus.DoesNotExist :
            notifStatus = False
        if not notifStatus :
            totalUnread = totalUnread + 1
        jsonData.append({
            'pk' :d.id,
            'notify_detail' :d.notif_msg,
            'notifStatus' :notifStatus
        })
    return render(request, 'trainer/notifs.html', {'notifs' :jsonData, 'totalUnread' :totalUnread})


# Mark Read By trainer
def mark_read_trainer_notif(request) :
    notif = request.GET['notif']
    notif = models.TrainerNotification.objects.get(pk=notif)
    trainer = models.Trainer.objects.get()
    models.NotifTrainerStatus.objects.create(notif=notif, trainer=trainer, status=True)

    # Count Unread
    totalUnread = 0
    data = models.TrainerNotification.objects.all()
    for d in data :
        try :
            notifStatusData = models.NotifTrainerStatus.objects.get(trainer=trainer, notif=d)
            if notifStatusData :
                notifStatus = True
        except models.NotifTrainerStatus.DoesNotExist :
            notifStatus = False
        if not notifStatus :
            totalUnread = totalUnread + 1

    return JsonResponse({'bool' :True, 'totalUnread' :totalUnread})


# Trainer Messages
def trainer_msgs(request) :
    data = models.TrainerMsg.objects.all().order_by('-id')
    return render(request, 'trainer/msgs.html', {'msgs' :data})


# Report for user
def report_for_user(request) :
    trainer = models.Trainer.objects.get()
    msg = ''
    if request.method == 'POST' :
        form = forms.ReportForUserForm(request.POST)
        if form.is_valid() :
            new_form = form.save(commit=False)
            new_form.report_from_trainer = trainer
            new_form.save()
            msg = 'Data has been saved'
        else :
            msg = 'Invalid Response!!'
    form = forms.ReportForUserForm
    return render(request, 'report_for_user.html', {'form' :form, 'msg' :msg})


# Report for trainer
def report_for_trainer(request) :
    user = request.user
    msg = ''
    if request.method == 'POST' :
        form = forms.ReportForTrainerForm(request.POST)
        if form.is_valid() :
            new_form = form.save(commit=False)
            new_form.report_from_user = user
            new_form.save()
            msg = 'Data has been saved'
        else :
            msg = 'Invalid Response!!'
    form = forms.ReportForTrainerForm
    return render(request, 'report_for_trainer.html', {'form' :form, 'msg' :msg})


def contact_page(request) :
    return render(request, 'contact_us.html')


def video(request) :
    obj = YouTube.objects.all()
    return render(request, 'video.html', {'obj' :obj})


