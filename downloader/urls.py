from django.urls import path
from .views import UrlCreateView, req_vid, download,howto_view, contact,privacy, terms

urlpatterns = [
    path('', UrlCreateView.as_view(), name='download'),
    path('download/', req_vid, name='download_page'),
    path('downloadvid/', download, name='download_video'),
    path('instructions/', howto_view, name='How-to'),
    path("contact/", contact, name="contact"),
    path("privacy-policy/", privacy, name="privacy"),
    path("Tos/", terms, name="terms")
    ]