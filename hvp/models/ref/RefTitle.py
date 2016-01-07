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

class RefTitle (models.Model):
    ID = models.AutoField( primary_key = True )
    Title = models.CharField('Title', max_length=20, blank=True)
    
    def __unicode__(self):
        return self.Title
    
    class Meta:
        app_label = 'hvp'
