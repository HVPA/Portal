################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 841 $
# Last Modified: $Date: 2014-06-06 15:55:03 +1000 (Fri, 06 Jun 2014) $ 
#
# === Description ===
#
#
################################################################################
from Portal import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from Portal.hvp.models.search import *
from Portal.hvp.models.users.LaboratoryGroup import LaboratoryGroup
from django.contrib.auth.models import User
import locale, jwt
from Portal.hvp.models.ref import RefTitle, RefState, RefUsageIntention

def get_node_stats():
    # used to provide the commas in the numbers display
    locale.setlocale(locale.LC_ALL, "")
    
    lab_count = locale.format('%d', len(Organisation.objects.all()), True)
    gene_count = locale.format('%d', len(Variant.objects.all().values("Gene").distinct()), True) # Only count genes with data
    variant_count = locale.format('%d', len(Variant.objects.all()), True)
    variant_instance_count = locale.format('%d', len(VariantInstance.objects.all()), True)
    user_count = locale.format('%d', len(User.objects.all()), True)
    organisation_count = locale.format('%d', len(LaboratoryGroup.objects.all()), True)
   
	# TODO: Make more elegant. Trying to get around the stupid 1 level access in django view of structures 
    return [{'Labs submitting': lab_count},
        {'Genes': gene_count},
        {'Unique Variants': variant_count},
        {'Instances submitted': variant_instance_count},
        {'Registered Users': user_count}]

def aaf_auth_view(request):
    if "assertion" in request.POST:
        # decoding assertion post using secret key
        verified_jwt = jwt.decode(request.POST['assertion'], settings.AAF_SECRET)
        
        # get basic info from the aaf jwt
        email = verified_jwt['https://aaf.edu.au/attributes']['mail']
        firstName = verified_jwt['https://aaf.edu.au/attributes']['givenname']
        lastName = verified_jwt['https://aaf.edu.au/attributes']['surname']
        
        # check user is in system sign user up for account if not
        if email != '':
            user = None
            try:
                # match user email with HVP db
                user = User.objects.get(email=email)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                
                # get node stats and return user to home page 
                node_stats = get_node_stats()
                
                return render_to_response('home/index.html', {'user':user, 'node_stats': node_stats,})
                
            except:
                # get ref data for signup page
                title_list = RefTitle.objects.all()
                state_list = RefState.objects.all()
                usage_list = RefUsageIntention.objects.all()
                
                # send user to signup page with their name and email pre-filled
                return render_to_response('users/signup.html', 
                                            {
                                                'firstName': firstName,
                                                'lastName': lastName,
                                                'user_email': email,
                                                'title_list': title_list,
                                                'state_list': state_list,
                                                'usage_list': usage_list,
                                            })
        
    else:
        return HttpResponseRedirect('/')

def index_view(request):
    # init var
    user = None
    error_message = None

    # get status data
    node_stats = get_node_stats()
    
    username = ''
    if request.method == 'POST':
        # try and get username and password from request to validate user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
            
        if user is not None:
            # login success
            login(request, user)
        else:
            # Error invalid login
            error_message = 'Invalid username or password'
    else:
        if request.user.is_authenticated():
            user = request.user

    return render_to_response('home/index.html',
                              {
                               'user': user,
                               'username': username,
                               'error_message': error_message,
                               'node_stats': node_stats,
                               })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def about_view(request):
    if request.user.is_authenticated():
        return render_to_response('home/about.html', {'user': request.user,})
    else:
        return render_to_response('home/about.html')

def policy_view(request):
    if request.user.is_authenticated():
        return render_to_response('home/policy.html', {'user': request.user,})
    else:
        return render_to_response('home/policy.html')
    
def contact_view(request):
    if request.user.is_authenticated():
        return render_to_response('home/contact.html', {'user': request.user,})
    else:
        return render_to_response('home/contact.html')

