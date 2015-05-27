################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: AlanLo $
# Last Revision: $Rev: 558 $
# Last Modified: $Date: 2011-08-24 13:43:55 +1000 (Wed, 24 Aug 2011) $ 
#
# === Description ===
#
#
################################################################################

from Portal.hvp.models import ref, users, search, labs
from django.contrib import admin

# Ref models
admin.site.register(ref.RefAccessStatus)
admin.site.register(ref.RefAllele)
admin.site.register(ref.RefDataType)
admin.site.register(ref.RefEthnicity)
admin.site.register(ref.RefLabRequestStatus)
admin.site.register(ref.RefPathogenicity)
admin.site.register(ref.RefPhenotypeFeature)
admin.site.register(ref.RefPhenotypeMethod)
admin.site.register(ref.RefSampleSource)
admin.site.register(ref.RefSampleTissue)
admin.site.register(ref.RefState)
admin.site.register(ref.RefTestMethod)
admin.site.register(ref.RefTitle)
admin.site.register(ref.RefUsageIntention)
admin.site.register(ref.RefVariantClass)

# User models
admin.site.register(users.Consensus)
admin.site.register(users.InstitutionContact)
admin.site.register(users.LaboratoryGroup)
admin.site.register(users.LabRequest)
admin.site.register(users.UserDocument)
admin.site.register(users.UserInstitution)
admin.site.register(users.UserProfile)

# Search models
admin.site.register(search.Gene)
admin.site.register(search.GrhaniteHash)
admin.site.register(search.HG_Build)
admin.site.register(search.Organisation)
admin.site.register(search.Patient)
admin.site.register(search.Phenotype)
admin.site.register(search.Variant)
admin.site.register(search.VariantInstance)
