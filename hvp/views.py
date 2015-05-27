################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 627 $
# Last Modified: $Date: 2013-07-15 14:20:00 +1000 (Mon, 15 Jul 2013) $ 
#
# === Description ===
#
#
################################################################################

from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from genename_reader import genename_reader

# txt filename that contains the gene names
# file needs to be in the same directory
filename = 'genes.txt'

# For importing gene data from www.genenames.org
def import_gene_view(request):
    # user is logged in
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
    
    # user is admin
    if not request.user.get_profile().IsHVPAdmin:
        raise Http404("You shouldn't here!")        

    # import genenames from txt file
    if 'import' in request.POST:
        reader = genename_reader('hvp/' + filename)
        reader.read();

        return render_to_response('hvp/import_gene_result.html', { 'blah': reader.entries, 'user': request.user })
    
    # takes user back home
    if 'cancel' in request.POST:
        #return render_to_response('home/index.html')
        return HttpResponseRedirect('/')
    
    return render_to_response('hvp/import_gene.html', {'user': request.user})



