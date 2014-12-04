################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 290 $
# Last Modified: $Date: 2011-03-17 11:21:15 +1100 (Thu, 17 Mar 2011) $ 
#
# === Description ===
#
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.models import User
from Portal.hvp.models import ref
from Portal.hvp.models.users.LaboratoryGroup import LaboratoryGroup
from Portal.hvp.models.users.UserProfile import UserProfile

# Adding a new org to user
def add_admin_laboratory_group_view(request, userID):
    if request.user.is_authenticated():
        if request.user.get_profile().IsHVPAdmin:
            # get ref state data
            state_list = ref.RefState.objects.all()
            
            # get user object
            user_object = get_object_or_404(User, pk=userID)
            user_profile = get_object_or_404(UserProfile, user=user_object)
            
            # init vars
            org_name = ''; org_address = ''; org_city= ''; org_post = ''
            org_phone = ''; org_fax = ''; org_state = ''
            org_name_exist = None
            add_save = True # for adding a new org and saving it to user
            
            if 'save' in request.POST:
                # get the post values
                org_name = request.POST['org_name']
                org_address = request.POST['org_address']
                org_city = request.POST['org_city']
                org_post = request.POST['org_post']
                org_phone = request.POST['org_phone']
                org_fax = request.POST['org_fax']
                org_state = request.POST['org_state']
                
                # check if organisation name already exist
                lab_group_list = LaboratoryGroup.objects.filter(Name__iexact = request.POST['org_name'])
                if len(lab_group_list) != 0:
                    org_name_exist = request.POST['org_name']
                else:
                    try:
                        lab_group = LaboratoryGroup()
                        lab_group.Name = org_name
                        lab_group.Address = org_address
                        lab_group.City = org_city
                        lab_group.PostCode = org_post
                        lab_group.Phone = org_phone
                        lab_group.Fax = org_fax
                        
                        if (org_state):
                            lab_group.State = ref.RefState.objects.get(State__iexact = org_state)
                        
                        # save and add to user
                        lab_group.save()
                        user_profile.LaboratoryGroup = lab_group
                        user_profile.save()
                        
                        return HttpResponseRedirect('/user_management/' + str(user_object.id) + '/')
                    
                    except:
                        if lab_group.id != None:
                            lab_group.delete()
                            
                        raise Http404('Something has gone horribly wrong! Please try again or contact the HVP system admin.')
                
            return render_to_response('users/laboratory_group.html',
                                      {
                                       'user_id': userID,
                                       'org_name': org_name,
                                       'org_address': org_address,
                                       'org_city': org_city,
                                       'org_post': org_post,
                                       'org_phone': org_phone,
                                       'org_fax': org_fax,
                                       'org_state': org_state,
                                       'user': request.user,
                                       'user_object': user_object,
                                       'state_list': state_list,
                                       'add_save': add_save,
                                       'org_name_exist': org_name_exist,
                                       })
        else:
            return Http404("You're no admin!!! You should not be here!")
    else:
        return render_to_response('home/timeout.html')

# view and edit organisation from admin
def admin_laboratory_group_view(request, userID, adminOrgID):
    if request.user.is_authenticated():
        if request.user.get_profile().IsHVPAdmin:
            # get ref state data
            state_list = ref.RefState.objects.all()
            
            # get user object
            user_object = get_object_or_404(User, pk=userID)
            
            # get admin organisation
            lab_group = get_object_or_404(LaboratoryGroup, pk=adminOrgID)
            
            # init vars
            org_name = lab_group.Name 
            org_address = lab_group.Address
            org_city = lab_group.City 
            org_post = lab_group.PostCode
            org_phone = lab_group.Phone
            org_fax = lab_group.Fax
            org_state = lab_group.State
            
            org_name_exist = None
            user_view_edit = True # for viewing and editing existing org
            
            if 'save' in request.POST:
                lab_group.Name = request.POST['org_name']
                lab_group.Address = request.POST['org_address']
                lab_group.City = request.POST['org_city']
                lab_group.PostCode = request.POST['org_post']
                lab_group.Phone = request.POST['org_phone']
                lab_group.Fax = org_fax = request.POST['org_fax']
                
                org_state = request.POST['org_state']
                if (org_state):
                    lab_group.State = ref.RefState.objects.get(State__iexact = org_state)
                
                # save and add to user
                lab_group.save()
                
                    
                return HttpResponseRedirect('/user_org/user/' + str(user_object.id))
            
            return render_to_response('users/laboratory_group.html',
                                      {
                                       'org_name': org_name,
                                       'org_address': org_address,
                                       'org_city': org_city,
                                       'org_post': org_post,
                                       'org_phone': org_phone,
                                       'org_fax': org_fax,
                                       'org_state': org_state,
                                       'user': request.user,
                                       'user_object': user_object,
                                       'state_list': state_list,
                                       'user_view_edit': user_view_edit,
                                       'org_name_exist': org_name_exist,
                                       })
        else:
            return Http404("You're no admin!!! You should not be here!")
    else:
        return render_to_response('home/timeout.html')