################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 790 $
# Last Modified: $Date: 2014-03-06 10:29:44 +1100 (Thu, 06 Mar 2014) $ 
#
# === Description ===
#
#
################################################################################

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from Portal.hvp.models.search.Patient import Patient
from Portal.hvp.models.search.Gene import Gene
from Portal.hvp.models.search.Variant import Variant
from Portal.hvp.models.search.VariantInstance import VariantInstance

import urllib

from Portal.search.hgvs_parser.Parser import Parser
from Portal.search.hgvs_parser.Validator import Validator

from Portal import settings
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Default view selects all Variants
def variant_view(request, geneID, path_filter, path_filter_ratio):
    template = 'variant'
    
    # kick user if they are not authenticated    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
    
    # kick user if they have not been verified
    if not request.user.get_profile().AccessStatus.ID == 2:
        return render_to_response('home/permission.html', {'user': request.user})

    # searching/filtering for a specific variant search
    if 'search' in request.POST:
        if request.POST['searched_variant'] != '':
            #search_type = request.POST['search_type']
            search_type = "variantType"            
            searched_variant = request.POST['searched_variant']
            return HttpResponseRedirect('/search/gene/' + geneID + 
                                        '/searchvariant/' + 
                                        urllib.quote(searched_variant) +
                                        '/' + search_type + '/results/' + path_filter + 
                                        '/' + path_filter_ratio + '/')
                                        
    # apply path filters (filter the path set by community consensus)
    dict_path = Dict_path_filter(path_filter)
    # apply path filter
    path_id = Path_ID(path_filter)
    
    # apply path filters ratio (the total number of instance per path)
    dict_path_ratio = Dict_path_filter(path_filter_ratio)
    # apply path filter ratio
    path_ratio_id = Path_ID(path_filter_ratio)
    
    # use gene name for query
    geneName = Gene.objects.get(pk=geneID).GeneName
    
    # query options to filter by community consensus path
    path_query_string = ''
    params = [geneName]
    if path_id != '':
        if path_id == 'NULL':
            path_query_string = ' and hvp_variant.Pathogenicity_id is NULL '
        else:
            path_query_string = ' and hvp_variant.Pathogenicity_id = %s '
            params = [geneName, path_id]
    
    # query options filter by path count
    count_query_string = ''
    order_query_string = ' order by Instances desc '
    if path_ratio_id != '':
        count_query_string = """, (select count(hvp_variantinstance.Pathogenicity_id) as path 
                            from hvp_variantinstance 
                            where hvp_variantinstance.Variant_ID = hvp_variant.ID 
                            and hvp_variantinstance.pathogenicity_id = """ + str(path_ratio_id) + ') as Path_Count '
        order_query_string = ' order by Path_Count desc '

    query = """select hvp_variant.*, Count(hvp_variantinstance.Variant_id) as Instances, 
                max(hvp_variantinstance.DateSubmitted) as DateSubmitted """ + count_query_string + """
                from hvp_variant
                left join hvp_variantinstance on hvp_variant.ID = hvp_variantinstance.Variant_id
                left join hvp_gene on hvp_variant.Gene_id = hvp_gene.ID
                where hvp_gene.GeneName = %s
                """ + path_query_string + ' group by ID ' + order_query_string
    
    qs = Variant.objects.raw(query, params)

    # get gene name to query variants from the same genename group
    geneName = Gene.objects.get(pk=geneID).GeneName
    #variant_list = Variant.objects.filter(Gene__GeneName = geneName)
                              
    variant_list = list(qs)
    
    # sum of total results used to display on screen
    results = variant_list.count

    # sets the paginator with the list of objects and number of objects per page
    paginator = Paginator(variant_list, 10)
    
    # gets the current page
    
    page = request.GET.get('page')
    try:
        variants = paginator.page(page)
    except PageNotAnInteger:
        variants = paginator.page(1)
    except EmptyPage:
        variants = paginator.page(paginator.num_pages)

    return render_to_response('search/variant.html', 
                                { 
                                    'user' : request.user,
                                    'template': template, 
                                    'variants' : variants,
                                    'geneName' : geneName,
                                    'geneID' : geneID,
                                    'results' : results,
                                    'dict_path': dict_path,
                                    'path_filter': path_filter,
                                    'dict_path_ratio': dict_path_ratio,
                                    'path_filter_ratio': path_filter_ratio,
                                })    


def variant_results_view(request, geneID, searched_variant, search_type, path_filter, path_filter_ratio):
    template = 'variant_result'
    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
        
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', {'user': request.user})
        
    # searching/filtering for a specific variant search
    if 'search' in request.POST:
        if request.POST['searched_variant'] != '':
            #search_type = request.POST['search_type']
            search_type = "variantType"            
            searched_variant = request.POST['searched_variant']
            return HttpResponseRedirect('/search/gene/' + geneID + 
                                        '/searchvariant/' + 
                                        urllib.quote(searched_variant) +
                                        '/' + search_type + '/results/' + path_filter + 
                                        '/' + path_filter_ratio + '/')
        else:
            # go back to the default variant page that lists all variants
            return HttpResponseRedirect('/search/gene/' + geneID +
                                        '/searchvariant/path_all/path_all/')
    
    gene = get_object_or_404(Gene, pk = geneID)
    geneName = gene.GeneName            
    page_error = False
    search_tooShort = False
    invalid_variant = False
    
    # apply path filters
    dict_path = Dict_path_filter(path_filter)
    # apply path filter
    path_id = Path_ID(path_filter)
    
    # apply path filters ratio (the total number of instance per path)
    dict_path_ratio = Dict_path_filter(path_filter_ratio)
    # apply path filter ratio
    path_ratio_id = Path_ID(path_filter_ratio)
    
    # keep url safe version for path filter links
    searched_variant_safe = searched_variant
    
    # converting url string back to a proper variant nomenclature
    searched_variant = urllib.unquote(searched_variant)
    # search_type = searchType
    paginate_results = 5

    # check if the search query string is less than 2 characters, if so return error message to user
    if len(searched_variant) < 2:
        page_error = True
        search_tooShort = True

    # check if the entered variant is valid
    validator = Validator()
    if validator.validate(searched_variant) == False:
        page_error = True
        invalid_variant = True
    
    # if there are no errors then proceed with the query
    variant_list = []
    variants = None
    results = None
    
    if not page_error:    
        # Break down the searched_variant using variant_parser to use in search with solr
        # NB: I noticed that any values that have been broken down in the parser that 
        # has a '+' or '-' will be converted to a long int. 
        parser = Parser()
        variant = parser.parse('', searched_variant)
        
        # query options filter by community consensus path
        path_query_string = ''
        params = [geneName]
        variant_query_string = VariantQueryString(variant, params)
    
        if path_id != '':
            if path_id == 'NULL':
                path_query_string = ' and v.Pathogenicity_id is NULL '
            else:
                path_query_string = ' and v.Pathogenicity_id = %s '
                params.append(path_id)
            
        # query options filter by path count
        count_query_string = ''
        order_query_string = ' order by Instances desc '
        if path_ratio_id != '':
            count_query_string = """, (select count(hvp_variantinstance.Pathogenicity_id) as path
                                from hvp_variantinstance
                                where hvp_variantinstance.Variant_ID = v.ID
                                and hvp_variantinstance.pathogenicity_id = """ + str(path_ratio_id) + ') as Path_Count '
            order_query_string = ' order by Path_Count desc '
    
        query = 'select v.*, Count(hvp_variantinstance.Variant_id) as Instances' + count_query_string + """
                from hvp_variant v
                left join hvp_variantinstance on v.ID = hvp_variantinstance.Variant_id
                left join hvp_gene on v.Gene_id = hvp_gene.ID
                where hvp_gene.GeneName = %s 
                """ + path_query_string + variant_query_string + ' group by ID ' + order_query_string
        
        qs = Variant.objects.raw(query, params)                                
        variant_list = list(qs)

        # sum of total results used to display on screen            
        results = variant_list.count #len(variant_list)

        # sets the paginator with the list of objects and number of objects per page
        paginator = Paginator(variant_list, 10)

        # gets the current page
        page = request.GET.get('page')            
        try:
            variants = paginator.page(page)
        except PageNotAnInteger:
            variants = paginator.page(1)
        except EmptyPage:
            variants = paginator.page(paginator.num_pages)

    return render_to_response('search/variant.html', 
                            {
                               'user': request.user, 
                               'template': template,
                               'searched_variant': searched_variant, 
                               'searched_variant_safe': searched_variant_safe,
                               'page_error': page_error, 
                               'invalid_variant': invalid_variant,
                               'paginate_results': paginate_results, 
                               'geneName' : geneName,
                               'geneID' : geneID,
                               'search_type': search_type, 
                               'variants': variants,
                               'results': results, 
                               'search_tooShort': search_tooShort,
                               'path_filter': path_filter,
                               'dict_path': dict_path,
                               'dict_path_ratio': dict_path_ratio,
                               'path_filter_ratio': path_filter_ratio,
                            },
                              context_instance=RequestContext(request))
       

def variant_patient_view(request, geneID, variantID, instanceID, path_filter, path_filter_ratio):
    template = 'variant_patient'
    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
        
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', {'user': request.user})
    
    gene = get_object_or_404(Gene, pk = geneID)
    instance = get_object_or_404(VariantInstance, pk = instanceID)
    
    searched_variant = ''
    searched_variant_safe = ''
    variant_query_string = ''
    params = [instance.Patient_id]
    page_error = False
    search_tooshort = False
    invalid_variant = False
    
    # apply path filters
    dict_path = Dict_path_filter(path_filter)
    # apply path filter
    path_id = Path_ID(path_filter)
    
    # apply path filters ratio (the total number of instance per path)
    dict_path_ratio = Dict_path_filter(path_filter_ratio)
    # apply path filter ratio
    path_ratio_id = Path_ID(path_filter_ratio)
        
    # query options to filter by community consensus path
    path_query_string = ''
    if path_id != '':
        if path_id == 'NULL':
            path_query_string = ' and v.Pathogenicity_id is NULL '
        else:
            path_query_string = ' and v.Pathogenicity_id = %s '
            params.append(path_id)
    
    # search results
    if 'search' in request.POST:
        search_type = 'variantType' #request.POST['search_type']
        
        if request.POST['searched_variant'] != '':
            searched_variant = request.POST['searched_variant']
            
            seached_variant_safe = searched_variant # url friendly
            searched_variant = urllib.unquote(searched_variant) # raw form
            
            validator = Validator()
            if validator.validate(searched_variant) == False:
                page_error = True
                invalid_variant = True

            # if there are no errors then proceed with the query
            if not page_error: 
                parser = Parser()
                variant = parser.parse('', searched_variant) 
                
                # query options filter by community consensus path
                path_query_string = ''

                variant_query_string = VariantQueryString(variant, params)

    # query options filter by path count
    count_query_string = ''
    order_query_string = ' order by Instances desc '
    if path_ratio_id != '':
        count_query_string = """, (select count(hvp_variantinstance.Pathogenicity_id) as path
                            from hvp_variantinstance
                            where hvp_variantinstance.Variant_ID = v.ID
                            and hvp_variantinstance.pathogenicity_id = """ + str(path_ratio_id) + ') as Path_Count '
        order_query_string = ' order by Path_Count desc '
    
    query = """select v.*, hvp_variantinstance.Patient_id,
            	(select Count(hvp_variantinstance.Variant_id) as i from hvp_variantinstance 
	            left join hvp_variant on hvp_variantinstance.Variant_ID = hvp_variant.ID
	            where hvp_variant.ID = v.ID) as instances """ + count_query_string + """
            from hvp_variant v
            left join hvp_variantinstance on v.ID = hvp_variantinstance.Variant_id
            where hvp_variantinstance.Patient_id = %s 
            """ + path_query_string + variant_query_string + ' group by ID ' + order_query_string
    
    qs = Variant.objects.raw(query, params)
    
    variant_list = list(qs)
    
    # sum of total results used to display on screen
    results = len(variant_list)
    
    # sets the paginator with the list of objects and number objects per page
    paginator = Paginator(variant_list, 10)
    
    # gets the current page
    page = request.GET.get('page')
    try:
        variants = paginator.page(page)
    except PageNotAnInteger:
        variants = paginator.page(1)
    except EmptyPage:
        variants = paginator.page(paginator.num_pages)
    
    return render_to_response('search/variant.html',
                            {
                                'user': request.user,
                                'template': template,
                                'dict_path': dict_path,
                                'path_filter': path_filter,
                                'geneID': geneID,
                                'variantID': variantID,
                                'gene': gene,
                                'variants': variants,
                                'instance': instance,
                                'results': results,
                                'page_error': page_error,
                                'search_tooshort': search_tooshort, 
                                'invalid_variant': invalid_variant,
                                'searched_variant': searched_variant,
                                'searched_variant_safe': searched_variant_safe,
                                'dict_path_ratio': dict_path_ratio,
                                'path_filter_ratio': path_filter_ratio,
                            })


"""
    Because we can''t use '>' and '_' symbols in the urlpatterns variables
    we need to convert them to something more url friendly like '.gt.' and '.us.'
"""
def ConvertSymbolsToUrlFriendly(variant_string):
    count = 0
    while count < len(variant_string):
        if variant_string[count] == '?':
            variant_string = variant_string[:count] + '.qm.' + variant_string[count+1:]
            count += 4
        elif variant_string[count] == '_':
            variant_string = variant_string[:count] + '.us.' + variant_string[count+1:]
            count += 4
        elif variant_string[count] == '>':
            variant_string = variant_string[:count] + '.gt.' + variant_string[count+1:]
            count += 4
        elif variant_string[count] == '*':
            variant_string = variant_string[:count] + '.wc.' + variant_string[count+1:]
            count += 4
        elif variant_string[count] == ':':
            variant_string = variant_string[:count] + '.sc.' + variant_string[count+1:]
            count += 4
        elif variant_string[count] == ',':
            variant_string = variant_string[:count] + '.cm.' + variant_string[count+1:]
            count += 4
        else:
            count +=1

    return variant_string


"""
    So this converts the url friendly chars back to a symbol.
"""
def ConvertToSymbols(variant_string):
    count = 0
    while count < len(variant_string):    
        if variant_string[count] == '.':
            if variant_string[count:count+4] == '.qm.':
                variant_string = variant_string[:count] + '?' + variant_string[count+4:]
                count += 1
            elif variant_string[count:count+4] == '.us.':
                variant_string = variant_string[:count] + '_' + variant_string[count+4:]
                count += 1
            elif variant_string[count:count+4] == '.gt.':
                variant_string = variant_string[:count] + '>' + variant_string[count+4:]
                count += 1
            elif variant_string[count:count+4] == '.wc.':
                variant_string = variant_string[:count] + '*' + variant_string[count+4:]
                count += 1
            elif variant_string[count:count+4] == '.sc.':
                variant_string = variant_string[:count] + ':' + variant_string[count+4:]
                count += 1
            elif variant_string[count:count+4] == '.cm.':
                variant_string = variant_string[:count] + ',' + variant_string[count+4:]
                count += 1
            else:
                count += 1
        else:
            count += 1
            
    return variant_string
    

"""
    Generate query string to search for genomic positioning cDNA ranges
"""
def VariantQueryString(variant, params):
    variant_query_string = ''
    # cDNA
    if variant.v_type.lower() == 'c':
        # range value to search against eg: position = 100, search range will between 50 to 150        
        rangeValue = 50
    
        if variant.position:
            if variant.position != '*':
                variant_query_string = (' and v.Position BETWEEN ' + str(int(Remove_WC(variant.position))-rangeValue) 
                    + ' and ' + str(int(Remove_WC(variant.position))+rangeValue))
        
        if variant.position_intron:
            if variant.position_intron[1] != '*':
                variant_query_string = (variant_query_string + ' and v.PositionIntron BETWEEN ' 
                    + str(int(Remove_WC(variant.position_intron))-rangeValue) + ' and ' + str(int(Remove_WC(variant.position_intron))+rangeValue))

        if variant.range_lower:
            if variant.range_lower != '*': 
                variant_query_string = (' and v.LowerRange BETWEEN ' + str(int(Remove_WC(variant.range_lower))-rangeValue) 
                    + ' and ' + str(int(Remove_WC(variant.range_lower))+rangeValue))
        
        if variant.range_lower_intron:
            if variant.range_lower_intron[1] != '*':
                variant_query_string = (variant_query_string + ' and v.LowerRangeIntron BETWEEN ' 
                    + str(int(Remove_WC(variant.range_lower_intron))-rangeValue) + ' and ' + str(int(Remove_WC(variant.range_lower_intron))+rangeValue))

        if variant.range_upper:
            if variant.range_upper != '*':
                variant_query_string = (variant_query_string + ' and v.UpperRange BETWEEN ' 
                    + str(int(Remove_WC(variant.range_upper))-rangeValue) + ' and ' + str(int(Remove_WC(variant.range_upper))+rangeValue))

        if variant.range_upper_intron:
            if variant.range_upper_intron[1] != '*':
                variant_query_string = (variant_query_string + ' and v.UpperRangeIntron BETWEEN ' 
                    + str(int(Remove_WC(variant.range_upper_intron))-rangeValue) + ' and ' + str(int(Remove_WC(variant.range_upper_intron))+rangeValue))
        
        if variant.operator:
            if '*' in variant.operator:
                if '*>' in variant.operator:
                    variant_query_string = variant_query_string + ' and v.Operator like %s '
                    params.append('%' + variant.operator[1:])
                
                elif '>*' in variant.operator:
                    variant_query_string = variant_query_string + ' and v.Operator like %s '
                    params.append(variant.operator[0:2] + '%')
            else:
                variant_query_string = variant_query_string + ' and v.Operator = %s '
                params.append(variant.operator)
            
            if variant.operator_value:
                variant_query_string = variant_query_string + ' and v.OperatorValue = %s '
                params.append(variant.operator_value)

        # to be used as last resort if no range index exist for variant
        if variant_query_string == '':            
            variant_query_string = ' and v.cDNA like %s '
            params.append('%'+variant.ToString()+'%')
        
    # Genomic
    if variant.v_type.lower() == 'g' or variant.genomic_ref or variant.v_type == '':
        # range value to search against this will be larger than the cDNA range as genomic is generally a large value
        rangeValue = 1000
        if variant.genomic_ref:
            try:
                if 'chr' in variant.genomic_ref:
                    # get the ref id
                    ref_id = variant.genomic_ref[3:len(variant.genomic_ref)]
                    ref_id = '%'+ref_id+'%'
                    if ref_id.isdigit():
                        variant_query_string = (' and v.GenomicRefSeq LIKE "' + ref_id + '" ') 
                
                if 'nc_' in variant.genomic_ref:
                    ref = variant.genomic_ref.split('.')
                    # get the ref id 
                    ref_id = ref[0]
                
                    # get the ref ver
                    ref_ver = ''
                    if len(ref) > 1:
                        ref_ver = ref[1]
                    
                    if ref_id:
                        variant_query_string = ' and v.GenomicRefSeq = "' + ref_id + '" '
                    
                        if ref_ver:
                            variant_query_string = variant_query_string + ' and v.GenomicRefSeqVer = "' + ref_ver + '" ' 
            
            except:
                # reset the query string if fails
                variant_query_string = ''
        
        if variant.position:
            if variant_query_string != '*': 
                variant_query_string = variant_query_string + (' and v.GenomicPosition BETWEEN ' + str(int(variant.position)-rangeValue) 
                    + ' and ' + str(int(variant.position)+rangeValue))
            
                if variant.operator:
                    if '*' in variant.operator:
                        if '*>' in variant.operator:
                            variant_query_string = variant_query_string + ' and v.Operator like %s '
                            params.append('%' + variant.operator[1:])
                
                        elif '>*' in variant.operator:
                            variant_query_string = variant_query_string + ' and v.Operator like %s '
                            params.append(variant.operator[0:2] + '%')
                    else:
                        variant_query_string = variant_query_string + ' and v.Operator = %s '
                        params.append(variant.operator)
            
                    if variant.operator_value:
                        variant_query_string = variant_query_string + ' and v.OperatorValue = %s '
                        params.append(variant.operator_value)
        else:
            # to be used as last resort if no genomic position exist for variant
            variant_query_string = ' and v.genomic like %s '
            params.append('%'+variant.ToString()+'%')
    
    return variant_query_string


# removes the wildcard '*' from the search range so that the value can be used to query the db
def Remove_WC(wc_string):
    return wc_string.replace('*','')


def Path_ID(path_filter):
    path_id = ''
    if path_filter == 'path':
        path_id = 4
        
    if path_filter == 'not_path':
        path_id = 1
        
    if path_filter == 'likely_not_path':
        path_id = 2
        
    if path_filter == 'likely_path':
        path_id = 3
        
    if path_filter == 'unknown_path':
        path_id = 5
        
    if path_filter == 'not_class':
        path_id = 'NULL'
        
    return path_id

def Dict_path_filter(path_filter):
    dict_path_filter = {'path_all':'', 'path':'', 'not_path':'', 'likely_not_path':'', 'likely_path':'', 'unknown_path':'', 'not_class':''}
    
    return dict_filter(path_filter, dict_path_filter)
    
def dict_filter(filter, dict_filter):
    dict_filter[filter] = 'checked="checked"'
    
    return dict_filter
