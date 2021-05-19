from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name=models.CharField(max_length=122, blank=True, null=True)
    email=models.CharField(max_length=122, blank=True, null=True)
    phone=models.CharField(max_length=12, blank=True, null=True)
    desc=models.TextField(max_length=122, blank=True, null=True)
    date=models.DateField()

    def __str__(self):
        return self.name

class Preferences(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='main_user')
    choice1 = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='choice1')
    choice2 = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='choice2')
    choice3 = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='choice3')
    choice4 = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='choice4')
    choice5 = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='choice5')

    def __str__(self):
        return self.user.username