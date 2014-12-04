################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 228 $
# Last Modified: $Date: 2010-07-28 11:39:49 +1000 (Wed, 28 Jul 2010) $ 
#
# === Description ===
#
#
################################################################################

from django.db import models
from django.contrib.auth.models import User
from Portal.hvp.models.ref.RefPathogenicity import RefPathogenicity
from Portal.hvp.models.search.Variant import Variant

class Consensus (models.Model):
    Date = models.DateField( 'Date', blank = False, null = False)
    Comments = models.CharField( 'Comments', max_length=20000, blank = False, null = False )

    Pathogenicity = models.ForeignKey(RefPathogenicity)
    User = models.ForeignKey(User)
    Variant = models.ForeignKey(Variant)
    
    class Meta:
        app_label = 'hvp'