
from django.urls import path
from . views import csv_upload_view

urlpatterns = [
    path('', csv_upload_view, name='uploadcsv'),
]
