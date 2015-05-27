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
from Portal.hvp.models.search.Variant import Variant
from Portal.hvp.models.search.Patient import Patient
from Portal.hvp.models.search.Organisation import Organisation
from Portal.hvp.models import ref

class VariantInstance( models.Model ):
    ID = models.AutoField( primary_key = True )
    HashCode = models.CharField( 'Hash Code', max_length=255, blank = False, null = False )
    Variant = models.ForeignKey( Variant )
    InstanceDate = models.DateField( 'Instance Date', blank = False, null = True )
    PatientAge = models.IntegerField( 'Patient Age', blank = False, null = True )
    TestMethod = models.ForeignKey( ref.RefTestMethod, null = True )
    SampleTissue = models.ForeignKey( ref.RefSampleTissue, null = True )
    SampleSource = models.ForeignKey( ref.RefSampleSource, null = True )
    Pathogenicity = models.ForeignKey( ref.RefPathogenicity, blank = True, null = True )
    #Justification = models.CharField( 'Justification', max_length=32767, blank = True, null = True )
    Justification = models.CharField( 'Justification', max_length=20000, blank = True, null = True )
    SIFTScore = models.IntegerField( 'SIFT Score', blank = False, null = True)
    PubMed = models.CharField( 'Pub Med Identifier', max_length=255, blank = True, null = True )
    RecordedInDatabase = models.NullBooleanField( 'Recorded In Database', null = True )
    SampleStored = models.NullBooleanField( 'Sample Stored', null = True )
    PedigreeAvailable = models.NullBooleanField( 'Pedigree Available', null = True )
    VariantSegregatesWithDisease = models.NullBooleanField( 'Variant Segregates with Disease', null = True )
    HistologyStored = models.NullBooleanField( 'Histology Stored', null = True )
    DateSubmitted = models.DateField( 'Date Submitted', blank = False, null = True )
    Patient = models.ForeignKey( Patient )
    Organisation = models.ForeignKey( Organisation )
    
    def __unicode__(self):
        return str(self.ID)
    
    class Meta:
        app_label = 'hvp'
