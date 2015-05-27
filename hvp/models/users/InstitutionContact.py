################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: AlanLo $
# Last Revision: $Rev: 224 $
# Last Modified: $Date: 2010-07-27 18:02:35 +1000 (Tue, 27 Jul 2010) $ 
#
# === Description ===
#
#
################################################################################

from django.db import models
from Portal.hvp.models import ref
from Portal.hvp.models.users.UserInstitution import UserInstitution

class InstitutionContact (models.Model):
    ContactTitle = models.ForeignKey(ref.RefTitle, null=True)
    ContactFirstName = models.CharField('ContactFirstName', max_length=50, blank=False, null=False)
    ContactLastName = models.CharField('ContactLastName', max_length=50, blank=False, null=False)
    ContactPhone = models.CharField('ContactPhone', max_length=25, blank=False, null=False)
    ContactEmail = models.CharField('ContactEmail', max_length=100, blank=False, null=False)
    
    UserInstitution = models.ForeignKey(UserInstitution, unique=True)
    
    def __unicode__(self):
        return str(self.ContactFirstName + ' ' + self.ContactLastName)
    
    class Meta:
        app_label = 'hvp'