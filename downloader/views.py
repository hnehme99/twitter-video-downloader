import numpy as np
import datetime
from django.shortcuts import render, redirect
from django.http import FileResponse,  HttpResponse
from django.views.generic import (
    CreateView)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError

from .models import Url
from .forms import UrlForm, ContactForm
from .videodownload import request_video


class UrlCreateView(CreateView):
    template_name = "index.html"
    form_class = UrlForm
    queryset = Url.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        link = form.cleaned_data['link']
        download_link = request_video(link)
        return super().form_valid(form)


def req_vid(request):
    twitter_url = request.GET.get('url')

    if not twitter_url:
        messages.error(request, 'Error: Field is empty. Please paste a link.')
        return redirect('download')
    elif "https://twitter.com" not in twitter_url:
        messages.error(request, 'Error: This is not a Twitter Link!')
        return redirect('download')
    else:
        pass

    try:
        links, qualities, thumb, created_at, duration, user, type = request_video(twitter_url)
    except:
        messages.error(request, 'Error: Tweet not found! Make sure to paste a valid link.')
        return redirect('download')

    links_with_qualities = dict(zip(links, qualities))

    context = {
        'links_with_qualities': links_with_qualities,
        'thumb': thumb,
        'qualities': qualities,
        'links': links,
        'created_at': created_at,
        'duration': duration,
        'user': user,
        'type': type

    }
    return render(request, "download_page.html", context)


def download(request):
    link = request.GET.get('dlbutton')
    print(link)
    return FileResponse(open(link, 'rb'))


def howto_view(request):
    return render(request, "howto.html", {})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("download")

    form = ContactForm()
    return render(request, "contact.html", {'form': form})

def privacy(request):
    return render(request, 'privacy.html', {})

def terms(request):
    return render(request, 'terms.html', {})