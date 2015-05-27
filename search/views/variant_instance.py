################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 744 $
# Last Modified: $Date: 2014-01-21 17:11:04 +1100 (Tue, 21 Jan 2014) $ 
#
# === Description ===
#
#
################################################################################

from Portal import settings

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from Portal.hvp.models.search.Patient import Patient
from Portal.hvp.models.search.Gene import Gene
from Portal.hvp.models.search.Variant import Variant
from Portal.hvp.models.search.VariantInstance import VariantInstance
from Portal.hvp.models.users.Consensus import Consensus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# shows list of variant instance for a selected variant
def variant_instance_view(request, geneID, variantID, path_filter, sort_filter, order_filter):
    template = 'variant_instance'
    
    # kick user if the are not authenticated
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')

    # kick user if they have not been verified
    if not request.user.get_profile().AccessStatus.ID == 2:
        return render_to_response('home/permission.html', {'user': request.user})

    gene = get_object_or_404(Gene, pk = geneID)
    variant = get_object_or_404(Variant, pk = variantID)

    # retrieve/set filters
    dict_path_filter = Dict_path_filter(path_filter)
    dict_sort_filter = Dict_sort_filter(sort_filter)
    dict_order_filter = Dict_order_filter(order_filter)
    
    # apply path filter
    path_id = Path_ID(path_filter)
    
    # apply sort filter
    sort = Sort(sort_filter)
        
    # apply order filter
    order = Order(order_filter)
    
    # get variant consensus if exist
    try:
        consensus = variant.Pathogenicity.Pathogenicity
    except:
        consensus = None

    qs = VariantInstance.objects.filter(Variant = variant).order_by(order + sort)
    if path_id:    
        qs = qs.filter(Pathogenicity__ID = path_id)
    variant_instance_list = qs
    
    # get the last instance submitted date
    try:        
        vi = VariantInstance.objects.filter(Variant = variant).order_by('-DateSubmitted', '-InstanceDate')
        last_date_submitted = vi[0].DateSubmitted
        last_date_submitted_ID = vi[0].ID
    except:
        last_date_submitted = ''
        last_date_submitted_ID = ''
    
    # sum of total results used to display on screen
    result = variant_instance_list.count

    # sets the paginator with the list of objects and number of objects per page
    paginator = Paginator(variant_instance_list, 10)
    
    # gets the current page
    page = request.GET.get('page')            
    try:
        variant_instances = paginator.page(page)
    except PageNotAnInteger:
        variant_instances = paginator.page(1)
    except EmptyPage:
        variant_instances = paginator.page(paginator.num_pages)

    return render_to_response('search/variant_instance.html', 
                            { 
                                'user': request.user,
                                'template': template, 
                                'gene': gene, 
                                'variant': variant, 
                                'result': result,
                                #'variant_instance_list': variant_instance_list, 
                                'variant_instances': variant_instances,
                                #'paginate_results': paginate_results,
                                #'result_low': result_low, 
                                #'result_high': result_high,
                                #'sort_type': sort_type, 
                                #'order_by': order_by,
                                #'filter_type': filter_type, 
                                #'filter_text': filter_text,
                                'dict_path_filter': dict_path_filter,
                                'dict_order_filter': dict_order_filter,
                                'dict_sort_filter': dict_sort_filter,
                                'path_filter': path_filter,
                                'order_filter': order_filter,
                                'sort_filter': sort_filter,
                                'consensus': consensus,
                                'last_date_submitted': last_date_submitted,
                                'last_date_submitted_ID': last_date_submitted_ID,
                            },
                        context_instance=RequestContext(request))
        

# shows a selected variant instance
def variant_instance_detail_view(request, geneID, variantID, instanceID):
    template = 'variant_instance'
    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
        
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', {'user': request.user})

    gene = get_object_or_404(Gene, pk = geneID)
    variant = get_object_or_404(Variant, pk = variantID)
    variant_instance = get_object_or_404(VariantInstance, pk = instanceID)

    return render_to_response('search/variant_instance_detail.html',
                              {
                               'user': request.user, 
                               'template': template,
                               'gene': gene, 
                               'variant': variant, 
                               'variant_instance': variant_instance,
                           })
    
# shows all other variant instance for a selected patientID     
def variant_instance_patient_view(request, geneID, variantID, instanceID, path_filter, sort_filter, order_filter):
    template = 'variant_instance_patient'
    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
        
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', {'user': request.user})
    
    # get related obejcts
    gene = get_object_or_404(Gene, pk = geneID)
    variant = get_object_or_404(Variant, pk = variantID)
    variant_instance = get_object_or_404(VariantInstance, pk = instanceID)
    patient = get_object_or_404(Patient, pk = variant_instance.Patient.HashCode)
    
    # retrieve/set filters
    dict_path_filter = Dict_path_filter(path_filter)
    dict_sort_filter = Dict_sort_filter(sort_filter)
    dict_order_filter = Dict_order_filter(order_filter)
    
    # apply path filter
    path_id = Path_ID(path_filter)
    
    # apply sort filter
    sort = Sort(sort_filter)
        
    # apply order filter
    order = Order(order_filter)
        
    qs = VariantInstance.objects.filter(Variant = variant, Patient = patient).order_by(order + sort)
    if path_id:
        qs = qs.filter(Pathogenicity__ID = path_id)
    variant_instance_list = qs
    
    # sum of total results used to display on screen
    results = variant_instance_list.count
    
    # sets the paginator with the list of objects and number objects per page
    paginator = Paginator(variant_instance_list, 10)
    
    # gets the current page
    page = request.GET.get('page')
    try:
        variant_instances = paginator.page(page)
    except PageNotAnInteger:
        variant_instances = paginator.page(1)
    except EmptyPage:
        variant_instances = paginator.page(paginator.num_pages)
        
    return render_to_response('search/variant_instance.html',
                            {
                                'user': request.user,
                                'template': template,
                                'gene': gene,
                                'dict_path_filter': dict_path_filter,
                                'dict_sort_filter': dict_sort_filter,
                                'dict_order_filter': dict_order_filter,
                                'path_filter': path_filter,
                                'order_filter': order_filter,
                                'sort_filter': sort_filter,
                                'variant': variant,
                                'instanceID': instanceID,
                                'results': results,
                                'variant_instances': variant_instances,
                            })

# shows a selected variant instance for a selected patient
def variant_instance_detail_patient_view(request, geneID, variantID, instanceID):
    template = 'variant_instance_patient'
    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
        
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', {'user': request.user})

    gene = get_object_or_404(Gene, pk = geneID)
    variant = get_object_or_404(Variant, pk = variantID)
    variant_instance = get_object_or_404(VariantInstance, pk = instanceID)

    return render_to_response('search/variant_instance_detail.html',
                              {
                               'user': request.user, 
                               'template': template,
                               'gene': gene, 
                               'variant': variant, 
                               'variant_instance': variant_instance,
                           })
                           
                           
# shows all variant instances from a select variant and lab/org
def variant_instance_lab_view(request, geneID, variantID, instanceID, path_filter, sort_filter, order_filter):
    template = 'variant_instance_lab'
    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
        
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', {'user': request.user})
        
    # get related objects
    gene = get_object_or_404(Gene, pk=geneID)
    variant = get_object_or_404(Variant, pk=variantID)
    variant_instance = get_object_or_404(VariantInstance, pk=instanceID)
    
    # retrieve/set filters
    dict_path_filter = Dict_path_filter(path_filter)
    dict_sort_filter = Dict_sort_filter(sort_filter)
    dict_order_filter = Dict_order_filter(order_filter)
    
    # apply path filter
    path_id = Path_ID(path_filter)
    
    # apply sort filter
    sort = Sort(sort_filter)
        
    # apply order filter
    order = Order(order_filter)

    qs = VariantInstance.objects.filter(Variant = variant, Organisation = variant_instance.Organisation).order_by(order + sort)
    if path_id:
        qs = qs.filter(Pathogenicity__ID = path_id)
    variant_instance_list = qs
    
    # sum of total results used to display on screen
    result = variant_instance_list.count
    
    # sets the paginator with the list of objects and number objects per page
    paginator = Paginator(variant_instance_list, 10)
    
    # gets the current page
    page = request.GET.get('page')
    try:
        variant_instances = paginator.page(page)
    except PageNotAnInteger:
        variant_instances = paginator.page(1)
    except EmptyPage:
        variant_instances = paginator.page(paginator.num_pages)
    
    return render_to_response('search/variant_instance.html', 
                                {
                                    'user': request.user,
                                    'template': template,
                                    'dict_path_filter': dict_path_filter,
                                    'dict_sort_filter': dict_sort_filter,
                                    'dict_order_filter': dict_order_filter,
                                    'path_filter': path_filter,
                                    'order_filter': order_filter,
                                    'sort_filter': sort_filter,
                                    'gene': gene,
                                    'variant': variant,
                                    'instanceID': instanceID,
                                    'result': result,
                                    'variant_instances': variant_instances,
                                })
                                
                                
# shows a selected variant instance for a selected patient
def variant_instance_detail_lab_view(request, geneID, variantID, instanceID):
    template = 'variant_instance_lab'
    
    if not request.user.is_authenticated():
        return render_to_response('home/timeout.html')
        
    if request.user.get_profile().AccessStatus.ID != 2:
        return render_to_response('home/permission.html', {'user': request.user})

    gene = get_object_or_404(Gene, pk = geneID)
    variant = get_object_or_404(Variant, pk = variantID)
    variant_instance = get_object_or_404(VariantInstance, pk = instanceID)

    return render_to_response('search/variant_instance_detail.html',
                              {
                               'user': request.user, 
                               'template': template,
                               'gene': gene, 
                               'variant': variant, 
                               'variant_instance': variant_instance,
                           })
                                

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
        
    return path_id
    
def Sort(sort_filter):
    sort = 'InstanceDate'
    if sort_filter == 'sort_subdate':
        sort = 'DateSubmitted'
    
    if sort_filter == 'sort_age':
        sort = 'PatientAge'
    
    if sort_filter == 'sort_path':
        sort = 'Pathogenicity__Pathogenicity'
        
    return sort
    
def Order(order_filter):
    order = ''
    if order_filter == 'order_desc':
        order = '-'
    
    return order

def Dict_path_filter(path_filter):
    dict_path_filter = {'path_all':'', 'path':'', 'not_path':'', 'likely_not_path':'', 'likely_path':'', 'unknown_path':''}
    
    return dict_filter(path_filter, dict_path_filter)
    
def Dict_sort_filter(sort_filter):
    dict_sort_filter = {'sort_date':'', 'sort_subdate':'', 'sort_age':'', 'sort_path':''}
    
    return dict_filter(sort_filter, dict_sort_filter)

def Dict_order_filter(order_filter):
    dict_order_filter = {'order_asc':'', 'order_desc':''}
    
    return dict_filter(order_filter, dict_order_filter)
    
def dict_filter(filter, dict_filter):
    dict_filter[filter] = 'checked="checked"'
    
    return dict_filter
