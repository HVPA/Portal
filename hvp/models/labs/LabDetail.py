from django.db import models
from Portal.hvp.models import ref

class LabDetail( models.Model ):
    ID = models.AutoField( primary_key = True )
    Org_Name = models.CharField('Organisation Name', max_length=1024, blank = False, null = False)
    Lab_Name = models.CharField('Laboratory Name', max_length=1024, blank = True, null = True)
    Address_1 = models.CharField('Address 1', max_length=1024, blank = False, null = False)
    Address_2 = models.CharField('Address 2', max_length=1024, blank = True, null = True)
    City = models.CharField('City or suburb', max_length=1024, blank = False, null = False)
    Post = models.CharField('POST Code', max_length=4, blank = False, null = False)
    State = models.ForeignKey(ref.RefState)
    Org_Hash = models.CharField( 'Hash Code', max_length=255, blank = False, null = False)
    HVP_ID = models.IntegerField()

    class Meta:
        app_label = 'hvp'
