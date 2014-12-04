################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 880 $
# Last Modified: $Date: 2014-07-22 12:02:33 +1000 (Tue, 22 Jul 2014) $ 
#
# === Description ===
#
#
################################################################################

from django.db import models
from Portal.hvp.models.search.Gene import Gene
from Portal.hvp.models import ref

class Variant( models.Model ):    
    ID = models.AutoField( primary_key=True )
    Gene = models.ForeignKey( Gene )
    cDNA = models.CharField( 'cDNA', max_length=3276, blank = False, null = True )
    mRNA = models.CharField( 'mRNA', max_length=3276, blank = False, null = True )
    Genomic = models.CharField( 'Genomic', max_length=3276, blank = False, null = True )
    Protein = models.CharField( 'Protein', max_length=3276, blank = False, null = True )
    VariantClass = models.ForeignKey( ref.RefVariantClass )
    Location = models.CharField( 'Location', max_length=3276, blank = False, null = True )
    Comments = models.CharField( 'Comments', max_length=3276, blank = False, null = True )
    Pathogenicity = models.ForeignKey( ref.RefPathogenicity, blank = True, null = True )
    
    # genomic range
    CalculatedGenomic = models.CharField( 'CalculatedGenomic', max_length=3276, blank = False, null = True )
    GenomicPosition = models.FloatField( 'GenomicPosition', blank = True, null = True )
    GenomicRefSeq = models.CharField( 'GenomicRefSeq', max_length=255, blank = False, null = True )
    GenomicRefSeqVer = models.CharField( 'GenomicRefSeqVer', max_length=255, blank = False, null = True )
    
    # cDNA ranges
    Position = models.FloatField( 'Position', blank = True, null = True )
    PositionIntron = models.FloatField( 'PositionIntron', blank = True, null = True )
    LowerRange = models.FloatField( 'LowerRange', blank = True, null = True )
    LowerRangeIntron = models.FloatField( 'LowerRangeIntron', blank = True, null = True )
    UpperRange = models.FloatField( 'UpperRange', blank = True, null = True )
    UpperRangeIntron = models.FloatField( 'UpperRange', blank = True, null = True )
    Operator = models.CharField( 'Operator', max_length = 255 , blank = True, null = True )
    OperatorValue = models.CharField( 'OperatorValue', max_length = 255, blank = True, null = True )
    Allele = models.ForeignKey( ref.RefAllele, null = True )
    
    class Meta:
        app_label = 'hvp'
    
    # Counts the number of total instances for variant and returns number of instances
    def count_total_instance(self):
        from Portal.hvp.models.search.VariantInstance import VariantInstance
        list = VariantInstance.objects.filter(Variant = self)
        return len(list)
    
    # get the highest count of path
    def count_highest_path(self):
        from Portal.hvp.models.search.VariantInstance import VariantInstance
        query = """
                select hvp_variantinstance.ID
                from hvp_variantinstance
                left join hvp_variant on hvp_variantinstance.Variant_id = hvp_variant.ID
                where hvp_variant.ID = %s
                """
        params = [self.ID]
        
        qs = VariantInstance.objects.raw(query, params)
        viList = list(qs)
        
        from operator import itemgetter
        sorted_viList = sorted(viList, key=itemgetter(2), reverse=True)
        
    
    # Counts the number of total instances of a particular Pathogencity
    def count_instance(self, id):
        from Portal.hvp.models.search.VariantInstance import VariantInstance
        query = """
                select hvp_variantinstance.ID
                from hvp_variantinstance
                left join hvp_variant on hvp_variantinstance.Variant_id = hvp_variant.ID
                left join hvp_refpathogenicity on hvp_variantinstance.Pathogenicity_id = hvp_refpathogenicity.ID
                where hvp_variant.ID = %s and hvp_refpathogenicity.ID = %s
                """
        params = [self.ID, id]
        
        qs = VariantInstance.objects.raw(query, params)
        viList = list(qs)
        
        return len(viList)
    
    # Certainly Not Path
    def count_instance_not_path(self):
        return self.count_instance(1)

    # Unlikely Path
    def count_instance_unlikely_path(self):
        return self.count_instance(2)
    
    # Likely Path
    def count_instance_likely_path(self):
        return self.count_instance(3)

    # Certainly Path
    def count_instance_path(self):
        return self.count_instance(4)

    # Unknown
    def count_instance_unknown(self):
        return self.count_instance(5)
        
    # count number of each Data Type
    def count_dataType_list(self):
        # get all the DataTypes
        dataType_list = ref.RefDataType.objects.all()
        
        # list to store dataTypes and number of instances per datatype
        dataType_list_count = []
        
        # count all the variant instance datatypes 
        for dataType in dataType_list:
            # ignore the first row "Show All"
            if dataType.ID == 1:
                continue
            
            query = """
                    select hvp_variantinstance.ID
                    from hvp_variantinstance
                    left join hvp_variant on hvp_variantinstance.Variant_id = hvp_variant.ID
                    left join hvp_refdatatype on hvp_variantinstance.DataType_id = hvp_refdatatype.ID
                    where hvp_variant.ID = %s and hvp_refdatatype.ID = %s
                    """
            params = [self.ID, dataType.ID]
            
            from Portal.hvp.models.search.VariantInstance import VariantInstance
            
            qs = VariantInstance.objects.raw(query, params)
            count = len(list(qs))
            
            dataType_list_count.append((dataType, count))
        
        # count the unknowns (variant instances without a set datatype)
        query = """
                select hvp_variantinstance.ID
                from hvp_variantinstance
                left join hvp_variant on hvp_variantinstance.Variant_id = hvp_variant.ID
                left join hvp_refdatatype on hvp_variantinstance.DataType_id = hvp_refdatatype.ID
                where hvp_variant.ID = %s and hvp_refdatatype.ID = %s
                """
        params = [self.ID, 'NULL']
        qs = VariantInstance.objects.raw(query, params)
        count = len(list(qs))
        
        dataType_list_count.append(('Unknown', count))
            
        return dataType_list_count
        
        
