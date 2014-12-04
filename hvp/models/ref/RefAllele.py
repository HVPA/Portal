from django.db import models

class RefAllele( models.Model ):
    ID = models.AutoField( primary_key = True )
    Allele = models.CharField( 'Allele', max_length=255, blank = False, null = False )

    def __unicode__(self):
        return self.Allele
    
    class Meta:
        app_label = 'hvp'
