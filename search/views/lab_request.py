################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 726 $
# Last Modified: $Date: 2013-12-20 14:30:54 +1100 (Fri, 20 Dec 2013) $ 
#
# === Description ===
# Lab Request from user for the selected VariantInstance
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
#from Portal.hvp.models import search, users
from Portal.hvp.models.search.Gene import Gene
from Portal.hvp.models.search.Variant import Variant
from Portal.hvp.models.search.VariantInstance import VariantInstance
from Portal.hvp.models.users.LabRequest import LabRequest
from Portal.hvp.models.ref.RefLabRequestStatus import RefLabRequestStatus
import datetime
from django.core.mail import send_mail
from Portal import settings
import logging

logger = logging.getLogger(__name__)

def default_view(request, geneID, variantID, instanceID, template):    
    if not request.user.is_authenticated():
        return render_to_response('home/permission.html', {'user': request.user})
        
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/timeout.html')
            
    gene = get_object_or_404(Gene, pk = geneID)
    variant = get_object_or_404(Variant, pk = variantID)
    variant_instance = get_object_or_404(VariantInstance, pk = instanceID)
    page_error = False

    # try and get an existing lab_request for this variant_instance
    lab_request_List = (LabRequest.objects.filter(VariantInstance = variant_instance) 
                        & LabRequest.objects.filter(User = request.user))
    lab_request = ''

    # if not empty
    if len(lab_request_List) == 1:
        lab_request = lab_request_List[0]
    # can't be greater than 1,if so raise 404 except
    if len(lab_request_List) > 1:
        raise Http404('There seems to be more than 1 lab_request for this instance, there should be only 1')

    if 'submit' in request.POST:
        if not lab_request:
            justification = request.POST['justification']
            # check if justification was filled in and not just blank
            if justification != '':
                # create a new lab request 
                lab_request = LabRequest()
                lab_request.ApplicationDate = datetime.date.today()
                lab_request.Justification = justification

                # foreign keys
                lab_request.User = request.user
                lab_request.Gene = gene
                lab_request.Variant = variant
                lab_request.VariantInstance = variant_instance

                lab_request.LabRequestStatus = RefLabRequestStatus.objects.get(pk=1)

                lab_request.save()

                # send email
                send_request_email( request.user, variant)
            else:
                page_error = True

    return render_to_response('search/lab_request.html',
                              {
                               'user': request.user, 
                               'template': template,
                               'gene': gene, 
                               'variant': variant,
                               'page_error': page_error, 
                               'lab_request': lab_request, 
                               'variant_instance': variant_instance,
                               })
    
def lab_request_view(request, geneID, variantID, instanceID):
    template = 'lab_request'
    
    return default_view(request, geneID, variantID, instanceID, template)

        
def lab_request_patient_view(request, geneID, variantID, instanceID):
    template = 'lab_request_patient'
    
    return default_view(request, geneID, variantID, instanceID, template)
              

def lab_request_lab_view(request, geneID, variantID, instanceID):
    template = 'lab_request_lab'
    
    return default_view(request, geneID, variantID, instanceID, template)


# sends email to admin to notify a request has been made
def send_request_email(user, variant):
    fromEmail = settings.ADMIN_EMAIL
    toEmail = settings.ADMIN_EMAIL

    try:
        send_mail(
                    '[HVP]Request for Variant Instance', # subject
                    (
                        'A lab request has been made by: ' + user.first_name + ' ' + user.last_name +
                        '\nFor a Variant Instance from: ' + variant.Genomic + ' ' + variant.cDNA
                     ),
                    fromEmail,
                    [toEmail],
                    fail_silently = False
                )
    except Exception as ex:
        # log: could not send email to admin
        logger.error('Lab request email to admin from user ' + user.email + 'failed: ' + str(ex))
        