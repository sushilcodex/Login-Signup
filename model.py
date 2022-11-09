'''
/**
 *@copyright : ToXSL Technologies Pvt. Ltd. < www.toxsl.com >
 *@author     : Shiv Charan Panjeta < shiv@toxsl.com >
 *
 * All Rights Reserved.
 * Proprietary and confidential :  All information contained herein is, and remains
 * the property of ToXSL Technologies Pvt. Ltd. and its partners.
 * Unauthorized copying of this file, via any medium is strictly prohibited.
 *
 *
 */
 '''
 

from distutils.command.upload import upload
import os
from .constants import *
from django.db import models
from django.utils.encoding import smart_str
from django.http.response import HttpResponse
from django.contrib.auth.models import AbstractUser




"""
User Model
"""
class User(AbstractUser):
    username = models.CharField(max_length=150,blank=True, null=True,unique=True)
    full_name = models.CharField(max_length=150,null=True,blank=True)
    first_name = models.CharField(max_length=150,null=True,blank=True)
    last_name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField("email address", null=True, blank=True)
    mobile_no = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    role_id = models.PositiveIntegerField(default=USERS,choices=USER_ROLE,null=True, blank=True)
    state_id = models.PositiveIntegerField(default=ACTIVE, choices=USER_STATUS,null=True, blank=True)
    status = models.BooleanField(default=True)
    job_status= models.PositiveIntegerField(default=0, choices=JOB_APPLY_STATUS,null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    year_of_experience = models.CharField(max_length=2,blank=True,null=True)
    resume = models.FileField(upload_to='resume',blank=True,null=True)
    registration_no = models.CharField(max_length=60,blank=True,null=True,)
    is_verified = models.PositiveIntegerField(default=0,choices=IS_VERIFIED,null=True, blank=True)
    about_me = models.TextField()
    average_rating = models.CharField(max_length=10,blank=True, null =True)
    otp = models.CharField(max_length=255,blank=True,null=True)
    verify_otp = models.BooleanField(default=0)
    is_subscribe = models.BooleanField(default=0)
    applied_for = models.CharField(max_length=10,null=True,blank=True)
    user_to_rvt=models.BooleanField(default=0)
    features_approval = models.BooleanField(default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    country = models.CharField(max_length=255,blank=True,null=True)
    session_id = models.CharField(max_length=500,blank=True,null=True)
   
    