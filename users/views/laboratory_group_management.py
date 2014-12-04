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


from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from Portal.hvp.models.users.UserProfile import UserProfile
from Portal.hvp.models import ref
from Portal.hvp.models.users.LaboratoryGroup import LaboratoryGroup
from django.http import Http404

def add_laboratory_group_management_view(request, userID):
    if request.user.is_authenticated():
        if request.user.get_profile().IsHVPAdmin:
            # get all admin_orgs
            lab_group_list = LaboratoryGroup.objects.all()
            
            # displays controls to set an LaboratoryGroup to user
            select_org = True
            
            # get user object and user profile
            user_object = get_object_or_404(User, pk=userID)
            user_profile = get_object_or_404(UserProfile, user=user_object)
            
            if request.POST:
                # save admin org to user
                labGroupID = request.POST['labGroupID']
                user_profile.LaboratoryGroup = get_object_or_404(LaboratoryGroup, pk=labGroupID)
                user_profile.AccessStatus = get_object_or_404(ref.RefAccessStatus, pk=2)
                user_profile.save()
                
                return HttpResponseRedirect('/user_management/' + userID + '/')
            
            return render_to_response('users/laboratory_group_management.html',
                                      {
                                       'user': request.user,
                                       'select_org': select_org,
                                       'user_object': user_object,
                                       'lab_group_list': lab_group_list,
                                       })
        else:
            return Http404("You're no admin!!! You should not be here!")
    else:
        return render_to_response('home/timeout.html')
