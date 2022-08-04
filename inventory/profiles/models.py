from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from timezone_field import TimeZoneField
from inventory.settings import TIME_ZONE as default_timezone
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = TimeZoneField(default=default_timezone)

    @property
    def display_name(self):
        if not self.user.first_name or not self.user.last_name:
            return self.user.username
        return " ".join([self.user.first_name, self.user.last_name])

    def get_absolute_url(self):
        return reverse("profile:profile")


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
