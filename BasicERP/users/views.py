from email import message
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm


@login_required
def user_change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid:
            # TODO: update user
            form.save()
            update_session_auth_hash(request, form.user)
            message.success("Your password was changed")
            redirect(reverse("dashboard"))
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/password_change_form.html", {"form": form})


def user_reset_password(request):
    return render(request, "users/password_reset_form.html")


def user_reset(request, uid, token):
    return render(request, "users/reset.html")
