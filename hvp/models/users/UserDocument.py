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
from django.contrib.auth.models import User

class UserDocument(models.Model):
    ID = models.AutoField( primary_key = True, editable=False )
    file = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, editable=False, null = True)
    
    class Meta:
        app_label = 'hvp'