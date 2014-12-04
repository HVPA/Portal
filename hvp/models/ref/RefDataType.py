from django.db import models

class RefDataType( models.Model ):
    ID = models.AutoField( primary_key = True )
    DataType = models.CharField( 'DataType', max_length=255, blank = False, null = False )

    def __unicode__(self):
        return self.DataType

    class Meta:
        app_label = 'hvp'
