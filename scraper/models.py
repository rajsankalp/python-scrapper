from django.db import models

# Create your models here.


class Buss(models.Model):
    title = models.CharField(max_length=300,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    url = models.CharField(max_length=500,blank=True,null=True)
    page_num = models.IntegerField(blank=True,null=True)
    land= models.IntegerField(blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True)
    website = models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    status = models.IntegerField(default=0,blank=True,null=True)
    latitude = models.FloatField(default=0,blank=True,null=True)
    longitude = models.FloatField(default=0,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    mobile = models.CharField(max_length=50,blank=True,null=True)
    type = models.CharField(max_length=50,blank=True,null=True)
    tags = models.CharField(max_length=500,blank=True,null=True)
    zip = models.CharField(max_length=20,blank=True,null=True)

    facebook = models.CharField(max_length=300,blank=True,null=True)
    linkedin = models.CharField(max_length=300,blank=True,null=True)
    organization_name = models.CharField(max_length=300,blank=True,null=True)
    donation_detail = models.TextField(blank=True,null=True)
    availablity_json = models.TextField(blank=True,null=True)


    updated_at = models.DateTimeField(blank=True,null=True) 


    def __str__(self):
        return self.title  


        
        
