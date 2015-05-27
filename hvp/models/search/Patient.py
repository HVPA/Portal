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
from Portal.hvp.models.ref import RefEthnicity

class Patient( models.Model ):
    HashCode = models.CharField( 'Hash Code', primary_key = True, max_length=255, blank = False, null = False )
    Ethnicity = models.ForeignKey( RefEthnicity, blank = False, null = True )
    
    def __unicode__(self):
        return str(self.HashCode)
    
    class Meta:
        app_label = 'hvp'
