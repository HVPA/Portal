################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: AlanLo $
# Last Revision: $Rev: 215 $
# Last Modified: $Date: 2010-07-27 10:25:28 +1000 (Tue, 27 Jul 2010) $ 
#
# === Description ===
#
#
################################################################################


from django.db import models
from Portal.hvp.models.search.VariantInstance import VariantInstance
from Portal.hvp.models import ref

class Phenotype( models.Model ):
    ID = models.AutoField( primary_key=True )
    VariantInstance = models.ForeignKey( VariantInstance )
    PhenotypeFeature = models.ForeignKey( ref.RefPhenotypeFeature )
    PhenotypeMethod = models.ForeignKey( ref.RefPhenotypeMethod )
    PhenotypeValue = models.CharField( 'Phenotype Value', max_length=255, blank = False, null = False )
    
    class Meta:
        app_label = 'hvp'