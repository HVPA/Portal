################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 856 $
# Last Modified: $Date: 2014-06-25 16:51:33 +1000 (Wed, 25 Jun 2014) $ 
#
# === Description ===
#
#
################################################################################


from django.db import models
from Portal.hvp.models import ref
from taggit.managers import TaggableManager

class Gene( models.Model ):
    ID = models.AutoField( primary_key=True )
    GeneName = models.CharField( 'Gene Name', max_length=50, blank = False, null = False )
    GeneDescription = models.CharField( 'Gene Description', max_length = 255, blank = False, null = False )
    RefSeqName = models.CharField( 'RefSeq Name', max_length=50, blank = False, null = False )
    RefSeqVer = models.CharField( 'RefSeq Version', max_length=50, blank = True, null = True )
    RefSeqValidStart = models.DateField( 'RefSeq valid start date', null = True )
    RefSeqValidEnd = models.DateField( 'RefSeq valid end date', null = True )
    
    #www.genename.org
    HGNC_ID = models.CharField( 'HGNC ID', max_length=50, blank = False, null = True )
    AlternateSymbols = models.CharField( 'Alternate Symbol', max_length=255, blank = True, null = True )
    AlternateNames = models.CharField( 'Alternate Name', max_length=1024, blank = True, null = True )
    Chromosome = models.CharField( 'Chromosome', max_length=50, blank = True, null = True )
    PreviousSymbols = models.CharField( 'Previous Symbols', max_length=255, blank = True, null = True )
    PreviousNames = models.CharField( 'Previous Names', max_length=1024, blank = True, null = True )
    
    # References to genbank for visualisation
    GenBankName = models.CharField( 'GenBankName', max_length=50, blank = True, null = True )
    GenBankVer = models.CharField( 'GenBank Version', max_length=50, blank = True, null = True )
    
    #Diseases = models.CharField( 'Diseases', max_length = 1024, blank = False, null = False )
    DiseasesTags = TaggableManager()

    #Variants = models.ManyToMany(Variant)

    class Meta:
        app_label = 'hvp'
    
    
    # count the number of unique variants for gene
    def count_total_variants(self):
        from Portal.hvp.models.search.Variant import Variant
        list = Variant.objects.filter(Gene = self)
        return len(list)
        
