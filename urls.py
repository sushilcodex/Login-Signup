
from django.contrib import admin
from django.urls import path , include
from django.conf.urls import include, url
from django.conf import settings
from accounts.views import  AdminLoginView
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from chat.views import *
from django.views.static import serve


router = DefaultRouter()



urlpatterns = [
    url(r'^admin/login/', AdminLoginView.as_view()),
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    
]


'''
/**
 *@copyright : ToXSL Technologies Pvt. Ltd. < www.toxsl.com >
 *@author     : Shiv Charan Panjeta < shiv@toxsl.com >
 *
 * All Rights Reserved.
 * Proprietary and confidential :  All information contained herein is, and remains
 * the property of ToXSL Technologies Pvt. Ltd. and its partners.
 * Unauthorized copying of this file, via any medium is strictly prohibited.
 **/
'''
from .views import *
from .views_api import *
from django.urls import path
from django.conf import settings
from django.conf.urls import url


admin.autodiscover()

app_name = 'rvt_lvt'

urlpatterns = [
    url(r'$', test, name=''),
    path('', test, name=''),
]