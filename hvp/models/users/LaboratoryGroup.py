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
# For lengths refer to http://stackoverflow.com/questions/20958/list-of-standard-lengths-for-database-fields
#
################################################################################


from django.db import models
from Portal.hvp.models import ref

class LaboratoryGroup (models.Model):
    Name = models.CharField('Name', max_length=255, blank=False, null=False)
    Address = models.CharField('Address', max_length=255, blank=False, null=False)
    City = models.CharField('City', max_length=35, blank=False, null=False)
    State = models.ForeignKey(ref.RefState)
    PostCode = models.CharField('PostCode', max_length=20, blank=False, null=False)
    Phone = models.CharField('Phone', max_length=25, blank=False, null=False)
    Fax = models.CharField('Fax', max_length=25, blank=True, null=True)
    
    def __unicode__(self):
        return str(self.Name)
    
    class Meta:
        app_label = 'hvp'