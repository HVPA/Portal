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

class RefSampleSource( models.Model ):
    ID = models.AutoField( primary_key = True )
    SampleSource = models.CharField( 'Sample Source', max_length=50, blank = False, null = False )

    def __unicode__(self):
        return self.SampleSource
    
    class Meta:
        app_label = 'hvp'