################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 281 $
# Last Modified: $Date: 2011-03-15 12:03:12 +1100 (Tue, 15 Mar 2011) $ 
#
# === Description ===
#
#
################################################################################

from django.db import models
from django.contrib.auth.models import User
from Portal.hvp.models.search.Gene import Gene
from Portal.hvp.models.search.Variant import Variant
from Portal.hvp.models.search.VariantInstance import VariantInstance
from Portal.hvp.models.ref.RefLabRequestStatus import RefLabRequestStatus

class LabRequest (models.Model):
    ApplicationDate = models.DateField( 'ApplicationDate', blank = False, null = False )
    Justification = models.CharField( 'Justification', max_length=20000, blank = False, null = False )
    
    User = models.ForeignKey(User)
    Gene = models.ForeignKey(Gene)
    Variant = models.ForeignKey(Variant)
    VariantInstance = models.ForeignKey(VariantInstance, null = False)
    
    LabRequestStatus = models.ForeignKey(RefLabRequestStatus, null = False) # status of application
    StatusDateUpdated = models.DateField('StatusDateUpdated', blank = True, null = True) # if status has been changed, store the last date it was updated
    
    class Meta:
        app_label = 'hvp'
