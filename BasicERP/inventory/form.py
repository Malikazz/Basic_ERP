from django.forms import CharField, HiddenInput, ModelForm
from django import forms
from .models import Order, OrderDocument, OrderImage
from django.contrib.auth.models import Group
from tinymce.widgets import TinyMCE
