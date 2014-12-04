################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: AlanLo $
# Last Revision: $Rev: 558 $
# Last Modified: $Date: 2011-08-24 13:43:55 +1000 (Wed, 24 Aug 2011) $ 
#
# === Description ===
#
#
################################################################################

from django.db import models
from django.contrib.auth.models import User
from Portal.hvp.models.users.LaboratoryGroup import LaboratoryGroup
from Portal.hvp.models import ref

class UserProfile (models.Model ):
    Phone = models.CharField('Phone', max_length=25, blank=False, null=False)
    Mobile = models.CharField('Mobile', max_length=25, blank=True)
    IsHVPAdmin = models.NullBooleanField('Is HVP admin', null=True)
    IsLabLeader = models.NullBooleanField('Is Lab Leader', null=True)
    AccessStatus = models.ForeignKey(ref.RefAccessStatus, null=False)
    UsageIntention = models.ForeignKey(ref.RefUsageIntention, null=True)
    Title = models.ForeignKey(ref.RefTitle, null=True)    
    LaboratoryGroup = models.ForeignKey(LaboratoryGroup, null=True)
    JoomlaUser_id = models.IntegerField( 'Joomla User ID', blank = False, null = True )
    
    # NB: 'user' needs to start in lowercase for UserProfile to work
    user = models.ForeignKey(User, unique=True)
    
    class Meta:
        app_label = 'hvp'
