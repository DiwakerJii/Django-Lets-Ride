from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.IntegerField()
    user_type = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

class TravelInfo(models.Model):
    going_from = models.CharField(max_length=255)
    going_to = models.CharField(max_length=255)
    date_time = models.CharField(max_length=35)
    preferred_medium = models.CharField(max_length=255,blank=True,null=True)
    assets_quantity = models.IntegerField()
    assets_type = models.IntegerField()           # 1:Laptop, 2:Travel_bag, 3:Package
    assest_sensitivity = models.IntegerField()    # 1:Normal, 2:Sensitivity, 3:Highly Sensitivity
    delivered_to = models.CharField(max_length=255)
    created_by = models.IntegerField()            # User id
    accepted_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True)  # User id
    created = models.DateTimeField(auto_now_add=True)

class RideInfo(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    going_from = models.CharField(max_length=255)
    going_to = models.CharField(max_length=255)
    date_time = models.CharField(max_length=35)
    travel_medium = models.CharField(max_length=255)
    assets_quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

