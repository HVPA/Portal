################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 558 $
# Last Modified: $Date: 2013-10-28 14:43:55 +1100 (Monday, 28 Oct 2013) $ 
#
# === Description ===
#
#
################################################################################

from django.db import models
from Portal.hvp.models.search.Patient import Patient
from Portal.hvp.models.search.Organisation import Organisation

class GrhaniteHash( models.Model ):
    ID = models.AutoField( primary_key=True )
    HashType = models.CharField( 'HashType', max_length=255, blank = False, null = False )
    Hash = models.CharField( 'Hash', max_length=255, blank = False, null = False )
    AgrWeight = models.CharField( 'AgrWeight', max_length=255, blank = False, null = False )
    Grhanite_GUID = models.CharField( 'Grhanite', max_length=255, blank = False, null = False )
    Site =  models.ForeignKey( Organisation )
    PatientHash = models.ForeignKey( Patient )

    class Meta:
        app_label = 'hvp'
