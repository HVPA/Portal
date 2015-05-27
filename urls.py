################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 763 $
# Last Modified: $Date: 2014-02-06 11:18:49 +1100 (Thu, 06 Feb 2014) $ 
#
# === Description ===
#
#
################################################################################



from django.conf.urls.defaults import *
from Portal import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # basic home page stuff
    (r'^$', 'Portal.home.views.index_view'),
    (r'^login/$', 'Portal.home.views.index_view'),
    (r'^logout/$', 'Portal.home.views.logout_view'),
    #(r'^about/$', 'Portal.home.views.about_view'),
    (r'^policy/$', 'Portal.home.views.policy_view'),
    #(r'^contact/$', 'Portal.home.views.contact_view'),
    
    # aaf validation view
    (r'^aaf/$', 'Portal.home.views.aaf_auth_view'),
    
    # gene default page - displays top 5 genes in db
    (r'search/searchgene/$', 'Portal.search.views.gene.gene_view'),
    
    # gene search results
    (r'search/searchgene/results/$', 'Portal.search.views.gene.gene_results_view'),
    
    # variant default page - lists all variants for selected gene ordered by total variant instance 
    (r'search/gene/(?P<geneID>\d+)/searchvariant/(?P<path_filter>\w+)/(?P<path_filter_ratio>\w+)/$', 'Portal.search.views.variant.variant_view'),
    
    # variant search results    
    (r'search/gene/(?P<geneID>\d+)/searchvariant/(?P<searched_variant>[\w|\W]+)/(?P<search_type>\w+)/results/(?P<path_filter>\w+)/(?P<path_filter_ratio>\w+)/$', 
        'Portal.search.views.variant.variant_results_view'),
    
    # variant instance results
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/instance_result/(?P<path_filter>\w+)/(?P<sort_filter>\w+)/(?P<order_filter>\w+)/$', 
        'Portal.search.views.variant_instance.variant_instance_view'),

    # variant instance details
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/instance/(?P<instanceID>\d+)/$', 
        'Portal.search.views.variant_instance.variant_instance_detail_view'),
        
    # variants from patient ID
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/patient/(?P<instanceID>\d+)/(?P<path_filter>\w+)/(?P<path_filter_ratio>\w+)/$',
        'Portal.search.views.variant.variant_patient_view'),
    
    # variant instance from patient ID
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/patient/(?P<instanceID>\d+)/instance_result/(?P<path_filter>\w+)/(?P<sort_filter>\w+)/(?P<order_filter>\w+)/$',
        'Portal.search.views.variant_instance.variant_instance_patient_view'),
        
    # variant instance details from patient ID
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/patient/instance_detail/(?P<instanceID>\d+)/$',
        'Portal.search.views.variant_instance.variant_instance_detail_patient_view'),
        
    # variant instance from lab/org ID
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/lab/instance_result/(?P<instanceID>\d+)/(?P<path_filter>\w+)/(?P<sort_filter>\w+)/(?P<order_filter>\w+)/$',
        'Portal.search.views.variant_instance.variant_instance_lab_view'),
        
    # variant instance details from lab/org ID
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/lab/instance_detail/(?P<instanceID>\d+)/$',
        'Portal.search.views.variant_instance.variant_instance_detail_lab_view'),
            
    # lab request contact
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/instance/(?P<instanceID>\d+)/lab_request/$',
        'Portal.search.views.lab_request.lab_request_view'),
        
    # lab request contact - patient
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/patient/instance_detail/(?P<instanceID>\d+)/lab_request/$',
        'Portal.search.views.lab_request.lab_request_patient_view'),
        
    # lab request contact - lab
    (r'search/gene/(?P<geneID>\d+)/variant/(?P<variantID>\d+)/lab/instance_detail/(?P<instanceID>\d+)/lab_request/$',
        'Portal.search.views.lab_request.lab_request_lab_view'),
        
    # consensus - contains the urlpattern of the page user came before, will allow easier backwards navigation
    #(r'search/gene/(?P<geneID>\d+)/searchvariant/(?P<searchedVariant>[-+a-zA-Z0-9.]+)/(?P<searchType>\w+)/variant/(?P<variantID>\d+)/consensus/$',
    #    'Portal.search.views.consensus.consensus_view'),  
    (r'search/gene/(?P<geneID>\d+)/searchvariant/variant/(?P<variantID>\d+)/consensus/$',
        'Portal.search.views.consensus.consensus_view'),
    
    # user request change org
    (r'user/change_org/', 'Portal.users.views.change_org.change_org_view'),
    
    # user management
    (r'user/$', 'Portal.users.views.user_account.user_account_view'),
    (r'user_management/$', 'Portal.users.views.admin_user_management.admin_user_management_view'), # list of users
    (r'user_management/(?P<userID>\d+)/$', 'Portal.users.views.admin_user_account.admin_user_account_view'), # selection of a user
    (r'pending/$', 'Portal.users.views.pending.pending_view'),
    
    # set user to laboratory group
    (r'user_org/user/(?P<userID>\d+)/$', 'Portal.users.views.laboratory_group_management.add_laboratory_group_management_view'), # list org to add to user
    (r'user_org/user/(?P<userID>\d+)/add/$', 'Portal.users.views.admin_laboratory_group.add_admin_laboratory_group_view'), #add & save org to user
    (r'user_org/user/(?P<userID>\d+)/lab/(?P<adminOrgID>\d+)/$', 'Portal.users.views.admin_laboratory_group.admin_laboratory_group_view'), #view/edit
    
    # admin email
    (r'admin_email/', 'Portal.users.views.admin_email.admin_email_view'),

    # request applications listing
    # for admin
    (r'request/$', 'Portal.users.views.laboratory_request.admin_laboratory_request_view'),
    (r'request/(?P<labRequestID>\d+)/$', 'Portal.users.views.laboratory_request.admin_laboratory_request_page_view'),
   
    # for users
    (r'user/request/$', 'Portal.users.views.laboratory_request.user_laboratory_request_view'),
    (r'user/request/?P<labRequestID>\d+/$', 'Portal.users.views.laboratory_request.user_laboratory_request_page_view'),
    
    # user doc download - not working
    #(r'user/admin/(?P<userID>\d+)/download/$', 'Portal.users.views.admin_user_account.downloadfile'),
    
    # user signup
    (r'^signup/$', 'Portal.users.views.signup.signup_view'),
    
    # Data import
    (r'import/$', 'Portal.hvp.views.import_gene_view'),
)

# IMPORTANT: the following shouldn't be used in a production setting. 
# Django docs says: "this method is inefficient and insecure"
# Django docs suggest you should set up the apache to serve static files instead.
# for more info: http://docs.djangoproject.com/en/dev/howto/static-files/
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>.*)/$', 'django.views.static.serve', 
        {'document_root': settings.HOME_DIR}),
    )


