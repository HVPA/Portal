from django.db import models
from Portal.hvp.models import ref
from Portal.hvp.models.labs import LabDetail

class LabContact( models.Model ):
    ID = models.AutoField( primary_key = True )
    Title = models.ForeignKey(ref.RefTitle, null=True)
    First_Name = models.CharField('First Name', max_length=255, blank = False, null = False)
    Last_Name = models.CharField('Last Name', max_length=255, blank = False, null = False)
    Phone = models.CharField('Phone Number', max_length=255, blank = False, null = False)
    Mobile = models.CharField('Mobile Number', max_length=255, blank = True, null = True)
    Fax = models.CharField('Fax Number', max_length=255, blank = True, null = True)
    Email = models.CharField('Email Address', max_length=255, blank = False, null = False)
    Lab = models.ForeignKey(LabDetail)

    class Meta:
        app_label = 'hvp'
