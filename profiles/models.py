import uuid
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class UserProfile(models.Model):
    profile_id = models.CharField(max_length=32, null=False, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def _generate_profile_id(self):
        '''
        Generate a random, unique profile id using UUID
        '''
        return uuid.uuid4().hex.upper()

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        '''
        Create or update the user profile
        '''
        if created:
            UserProfile.objects.create(user=instance)
        # Existing users: just save the profile
        instance.userprofile.save()

    def save(self, *args, **kwargs):
        '''
        Save user profile with unique profile id using UUID
        '''
        if not self.profile_id:
            self.profile_id = self._generate_profile_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    profile_id = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True,
                                       default='')
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=10, null=True, blank=False)
    # limit delivery in just a country since this is food delivery
    country = models.CharField(
        max_length=40, null=False, blank=False, default='Norway')
    address_type = models.CharField(max_length=50, null=True, blank=True,
                                    default='Home')
    isDefault = models.BooleanField(default=False)

    def __str__(self):
        return self.street_address1 + ', ' + \
            self.town_or_city + ', ' + self.postcode + ' ' + self.country
