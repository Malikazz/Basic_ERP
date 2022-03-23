from django.core.mail import send_mail
from django.contrib.auth.models import User

def new_user(user:User) -> None:
  '''Sends a email to the new users registered email welcoming them'''
  return 0

def 