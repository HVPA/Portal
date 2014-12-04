################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 550 $
# Last Modified: $Date: 2011-07-01 12:38:20 +1000 (Fri, 01 Jul 2011) $ 
#
# === Description ===
#
# For lengths refer to http://stackoverflow.com/questions/20958/list-of-standard-lengths-for-database-fields
#
################################################################################

from django.db import models
from Portal.hvp.models import ref
from django.contrib.auth.models import User

class UserInstitution (models.Model):
    Name = models.CharField('Name', max_length=255, blank=False, null=False)
    Department = models.CharField('Department', max_length=255, blank=True, null=False)
    Address = models.CharField('Address', max_length=255, blank=False, null=False)
    City = models.CharField('City', max_length=35, blank=False, null=False)
    State = models.ForeignKey(ref.RefState)
    PostCode = models.CharField('PostCode', max_length=10, blank=False, null=False)
    Phone = models.CharField('Phone', max_length=25, blank=False, null=False)
    Fax = models.CharField('Fax', max_length=25, blank=True, null=True)
    StartDate = models.DateField('StartDate', blank = True, null = True)
    EndDate = models.DateField('EndDate', blank = True, null = True)
    ApplicationDate = models.DateField('ApplicationDate', blank = True, null = True) # TODO: Should be never blank/null

    Institution = models.OneToOneField(User, primary_key=False, null=True, related_name='Institution')
    
    CurrentInstitution = models.OneToOneField(User, primary_key=False, null=True, related_name='CurrentInstitution')
    PendingInstitution = models.OneToOneField(User, primary_key=False, null=True, related_name='PendingInstitution')
    BelongsTo = models.ForeignKey(User, related_name="InstitutionHistory")
    
    class Meta:
        app_label = 'hvp'
