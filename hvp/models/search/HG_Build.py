################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 728 $
# Last Modified: $Date: 2013-12-20 14:44:12 +1100 (Fri, 20 Dec 2013) $ 
#
# === Description ===
#
#
################################################################################


from django.db import models

class HG_Build( models.Model ):
    ID = models.AutoField( primary_key=True )
    BuildNumber = models.CharField( 'BuildNumber', max_length=255, blank = False, null = False )

    class Meta:
        app_label = 'hvp'
        