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
#
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404
from Portal.hvp.models.search.Gene import Gene
from Portal.hvp.models.search.Variant import Variant
from Portal.hvp.models.ref.RefPathogenicity import RefPathogenicity
from Portal.hvp.models.users.Consensus import Consensus
from django.http import Http404, HttpResponseRedirect
import datetime

def consensus_view(request, geneID, variantID):
    if request.user.is_authenticated():
        if request.user.get_profile().IsHVPAdmin:
            gene = get_object_or_404(Gene, pk = geneID)
            variant = get_object_or_404(Variant, pk = variantID)
            page_error = False
            
            # get list of path from ref table
            path_list = RefPathogenicity.objects.all() 
            
            # try and get an existing consensus for this variant
            consensus_list = (Consensus.objects.filter(Variant = variant) 
                                & Consensus.objects.filter(User = request.user))
            consensus = None
            # will be set to true to display saved message on screen after saving a consensus
            consensus_saved = False
            
            # if list not empty
            if len(consensus_list) == 1:
                consensus = consensus_list[0]
            if len(consensus_list) > 1:
                raise Http404('There seems to be more than 1 consensus for this variant, there should be only 1')
            
            if 'submit' in request.POST:
                comments = request.POST['comments']
                path =  request.POST['path']
                # check if comments was filled in and path is set
                if path != '':
                    # path is not empty get path from ref
                    ref_path = RefPathogenicity.objects.get(Pathogenicity__iexact = path)
                    
                    # set variant path
                    variant.Pathogenicity = ref_path
                    variant.save()
                    # for each item to be iterated
                    # save over existing consensus
                    if consensus:
                        consensus.Date = datetime.date.today()
                        consensus.Pathogenicity = ref_path
                        consensus.Comments = comments
                    else:
                        # create a new consensus
                        consensus = Consensus()
                        consensus.Date = datetime.date.today()
                        consensus.Pathogenicity = ref_path
                        consensus.Comments = comments
                        
                        # set foreign keys
                        consensus.User = request.user
                        #consensus.Gene = gene
                        consensus.Variant = variant
                        
                    # save object
                    consensus.save()
                    consensus_saved = True
                else:
                    page_error = True
            
            saved_path = ''
            if consensus:
                saved_path = consensus.Pathogenicity.Pathogenicity
            
            return render_to_response('search/consensus.html',
                                      {
                                       'user': request.user, 
                                       'gene': gene, 
                                       'variant': variant,
                                       'path_list': path_list,
                                       'page_error': page_error,
                                       'consensus': consensus,
                                       'saved_path': saved_path,
                                       'consensus_saved': consensus_saved,
                                       })
        else:
            raise Http404("You're no admin!!! You should not be here!")
    else:
        return render_to_response('home/timeout.html')