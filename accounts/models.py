import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models.signals import post_delete


def _display_pic_path(instance, filename):
  """Gets path to store display pic of the instance.

  Args: The instance.
  filename: The filename.

  Returns:
    The path to upload display pic.
  """
  ext = os.path.splitext(filename)[1]
  f_name = '%s%s' % (instance.username, ext)
  return os.path.join('avatars', f_name)


def _banner_pic_path(instance, filename):
  """Gets path to store banner pic of the instance.

  Args: The instance.
  filename: The filename.

  Returns:
    The path to banner display pic.
  """
  ext = os.path.splitext(filename)[1]
  f_name = 'banner_%s%s' % (instance.username, ext)
  return os.path.join('avatars', f_name)


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    country_code = models.CharField(max_length=3, default=91)
    mobile_number = models.CharField(max_length=10)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    aadhar = models.CharField(max_length=16, blank=True, null=True)
    is_employee = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    reg_status = models.BooleanField(default=False)


    #@property
    #def is_biller(self):
    #    return self.employee_type == 'BILL'

    def __unicode__( self ):
            return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)


class UserAddress(models.Model):
  user = models.ForeignKey(User)
  address = models.CharField(max_length=25, null =True)
  building_name = models.CharField(max_length=50, blank=True, null=True)
  road_name = models.CharField(max_length=30, blank=True, null=True)
  landmark = models.CharField(max_length=30, blank=True, null=True)
  area_name = models.CharField(max_length=25)
  city = models.CharField(max_length=25)
  pin = models.CharField(max_length=6)
  
  def get_absolute_url(self):
          return reverse('deleteAreaDetail','editAreaDetail',kwargs={"id": self.id})
