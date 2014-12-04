################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 881 $
# Last Modified: $Date: 2014-07-22 15:44:08 +1000 (Tue, 22 Jul 2014) $ 
#
# === Description ===
#
#
################################################################################

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from Portal.hvp.models.search.Gene import Gene
from Portal.hvp.models.search.Variant import Variant
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.utils import simplejson
from django.db.models import Q

from Portal.search.views.variant import ConvertSymbolsToUrlFriendly
import urllib

from Portal.search.hgvs_parser.Parser import Parser
from Portal.search.hgvs_parser.Validator import Validator

from Portal import settings

# Default Gene Page: Shows current top 5 genes in DB
def gene_view(request):
    # send user to timeout page if not authenticated    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
    
    # deny access if permission has not been granted
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', {'user': request.user, })
        
    page_error = False
    #user = request.user
    BASE_URL = settings.BASE_URL # for locals
    
    query = """
        select g1.*, max(hvp_variantinstance.DateSubmitted) as DateSubmitted,
        (select Count(hvp_variant.ID) as variants from hvp_variant
        left join hvp_gene g2 on hvp_variant.Gene_id = g2.ID
        where g2.GeneName = g1.GeneName) as Variants,

        (select Count(hvp_variantinstance.ID) as variantInstances from hvp_variantinstance
        left join hvp_variant on hvp_variantinstance.Variant_id = hvp_variant.ID
        left join hvp_gene on hvp_variant.Gene_id = hvp_gene.ID
        where hvp_gene.GeneName = g1.GeneName) as VariantInstances

        from hvp_gene g1
        left join hvp_variant on g1.ID = hvp_variant.Gene_id
        left join hvp_variantinstance on hvp_variant.ID = hvp_variantinstance.Variant_id
        group by GeneName
        order by Variants desc
        limit 5
        """
    qs = Gene.objects.raw(query)                                
    gene_list = list(qs)

    # set the search result into the url
    #if 'search' in request.POST:
    #    # get user gene search query from POST
    #    searched_gene = request.POST['searched_gene']

    """
    if len(searched_gene) < 2:
        #page_error = True
        #return HttpResponseRedirect(settings.BASE_URL + '/search/searchgene/' + '0' + '/results/')
        return HttpResponseRedirect(settings.BASE_URL + '/search/searchgene/results/')
    else:
        #return HttpResponseRedirect(settings.BASE_URL + '/search/searchgene/' + searched_gene + '/results/')
        return HttpResponseRedirect(settings.BASE_URL + '/search/searchgene/results/')
    """
    return render_to_response('search/gene.html', {'user':request.user, 'page_error':page_error, 'gene_list':gene_list, })


# Returns gene searched results
def gene_results_view(request):
    # send user to timeout page if not authenticated
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')

    # deny access if permission has not been granted    
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', { 'user': request.user })
    
    # default if blank search all
    searched_gene = ''
    if 'searched_gene' in request.POST:
        searched_gene = request.POST['searched_gene']

    #gene = searchedGene
    paginate_results = 5
    error = False
    # if searched_gene is genomic variant starting with "chr."(chromosome) or 'nc_'(refseq)
    # then we can go directy to the gene and searched for the variant in the variant page.
    if ('chr' in searched_gene.lower() or 'nc_' in searched_gene.lower()) and ':' in searched_gene.lower():
        # try and get the gene from the variant
        try:
            p = Parser()
            variant = p.parse('', searched_gene)
            variant.genomic_ref
            variant_list = []
            
            if 'nc_' in searched_gene.lower():   
                split_string = searched_gene.lower().split(':')[0].split('.')[0]
                variant_list = Variant.objects.filter(GenomicRefSeq = split_string)
            else:
                split_string = searched_gene.lower().split(':')[0].replace('chr','')
                variant_list = Variant.objects.filter(Q(GenomicRefSeq__contains=split_string))
                
            if variant_list >= 1:
                gene = variant_list[0].Gene
                
            return HttpResponseRedirect(settings.BASE_URL + '/search/gene/' + str(gene.ID) + '/searchvariant/' + 
                urllib.quote(searched_gene) + '/variantType/results/1/path_all/path_all/')
        except:
            error = True
                
    # tries for a precise search for the GeneName, groups then by GeneName due to duplicate GeneNames
    # with different RefSeq Names and Versions.
    #gene_list = (Gene.objects.filter(GeneName__istartswith=searched_gene).values('GeneName').distinct())
    if searched_gene == '':
        #qs = Gene.objects.all().order_by('GeneName')
        #qs.query.group_by = ['GeneName']
        #gene_list = qs
        query = """
            select g1.*, max(hvp_variantinstance.DateSubmitted) as DateSubmitted,

            (select Count(hvp_variant.ID) as variants from hvp_variant
            left join hvp_gene g2 on hvp_variant.Gene_id = g2.ID
            where g2.GeneName = g1.GeneName) as Variants,

            (select Count(hvp_variantinstance.ID) as variantInstances from hvp_variantinstance
            left join hvp_variant on hvp_variantinstance.Variant_id = hvp_variant.ID
            left join hvp_gene on hvp_variant.Gene_id = hvp_gene.ID
            where hvp_gene.GeneName = g1.GeneName) as VariantInstances

            from hvp_gene g1
            left join hvp_variant on g1.ID = hvp_variant.Gene_id
            left join hvp_variantinstance on hvp_variant.ID = hvp_variantinstance.Variant_id
            group by GeneName
            order by GeneName asc
        """
        qs = Gene.objects.raw(query)                                
        gene_list = list(qs)
    else:
        #qs = (Gene.objects.filter(GeneName__istartswith=searched_gene))
        #qs.query.group_by = ['GeneName']          
        #gene_list = qs
        query = """
            select g1.*, max(hvp_variantinstance.DateSubmitted) as DateSubmitted,
            
            (select Count(hvp_variant.ID) as variants from hvp_variant
            left join hvp_gene g2 on hvp_variant.Gene_id = g2.ID
            where g2.GeneName = g1.GeneName) as Variants,

            (select Count(hvp_variantinstance.ID) as variantInstances from hvp_variantinstance
            left join hvp_variant on hvp_variantinstance.Variant_id = hvp_variant.ID
            left join hvp_gene on hvp_variant.Gene_id = hvp_gene.ID
            where hvp_gene.GeneName = g1.GeneName) as VariantInstances

            from hvp_gene g1
            left join hvp_variant on g1.ID = hvp_variant.Gene_id
            left join hvp_variantinstance on hvp_variant.ID = hvp_variantinstance.Variant_id
            where GeneName like %s
            group by GeneName
            order by GeneName asc
        """
        qs = Gene.objects.raw(query, [searched_gene+'%'])
        gene_list = list(qs)

    # if nothing is return then we need to search in the other areas
    if len(gene_list) == 0:
        """
        qs = (Gene.objects.filter(RefSeqName__istartswith=searched_gene)
                                   | Gene.objects.filter(GeneDescription__istartswith=searched_gene)
                                   | Gene.objects.filter(HGNC_ID__istartswith=searched_gene) 
                                   | Gene.objects.filter(AlternateSymbols__istartswith=searched_gene) 
                                   | Gene.objects.filter(AlternateNames__istartswith=searched_gene)
                                   | Gene.objects.filter(Chromosome__istartswith=searched_gene)
                                   | Gene.objects.filter(PreviousSymbols__istartswith=searched_gene)
                                   | Gene.objects.filter(PreviousNames__istartswith=searched_gene))
        qs.query.group_by = ['GeneName']
        gene_list = qs
        """
        query = """
            select g1.*, max(hvp_variantinstance.DateSubmitted) as DateSubmitted,
            
            (select Count(hvp_variant.ID) as variants from hvp_variant
            left join hvp_gene g2 on hvp_variant.Gene_id = g2.ID
            where g2.GeneName = g1.GeneName) as Variants,

            (select Count(hvp_variantinstance.ID) as variantInstances from hvp_variantinstance
            left join hvp_variant on hvp_variantinstance.Variant_id = hvp_variant.ID
            left join hvp_gene on hvp_variant.Gene_id = hvp_gene.ID
            where hvp_gene.GeneName = g1.GeneName) as VariantInstances

            from hvp_gene g1
            left join hvp_variant on g1.ID = hvp_variant.Gene_id
            left join hvp_variantinstance on hvp_variant.ID = hvp_variantinstance.Variant_id
            where (RefSeqName like %s or GeneDescription like %s or HGNC_ID like %s 
            or AlternateSymbols like %s or AlternateNames like %s or Chromosome like %s 
            or PreviousSymbols like %s or PreviousNames like %s)
            group by GeneName
            order by GeneName asc
        """
        qs = Gene.objects.raw(query, [searched_gene+'%', '%'+searched_gene+'%', searched_gene+'%', '%'+searched_gene+'%', '%'+searched_gene+'%', searched_gene+'%', '%'+searched_gene+'%', '%'+searched_gene+'%'])
        gene_list = list(qs)
    # Calculate the mth and nth record numbers displayed for this page
    #result_low = max(1, (request.page - 1)*paginate_results + 1)
    #result_high = min(int(gene_list.count()), request.page*paginate_results)
    
    # if still nothing then look at the gene disease tags - using taggit
    if len(gene_list) == 0:
        # break down string into list
        searched_gene_list = searched_gene.split(' ')
        gene_list = Gene.objects.filter(DiseasesTags__name__in=searched_gene_list).distinct()
    
    # number genes returned from search
    gene_count = gene_list.count

    # sets the paginator with the list of objects and number of objects per page
    paginator = Paginator(gene_list, 10)          

    # gets the current page
    page = request.GET.get('page')            
    try:
        genes = paginator.page(page)
    except PageNotAnInteger:
        genes = paginator.page(1)
    except EmptyPage:
        genes = paginator.page(paginator.num_pages)

    return render_to_response('search/gene_result.html', 
            {
                'user': request.user, 
                'error': error,
                #'gene': gene, 
                'searched_gene': searched_gene,
                'gene_count': gene_count,
                'genes': genes,
                'paginate_results': paginate_results,
                #'result_low': result_low,
                #'result_high': result_high,
                'BASE_URL': settings.BASE_URL,
            },
        context_instance=RequestContext(request))

