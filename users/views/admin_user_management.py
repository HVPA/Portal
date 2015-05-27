################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 232 $
# Last Modified: $Date: 2010-07-29 12:04:46 +1000 (Thu, 29 Jul 2010) $ 
#
# === Description ===
#
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext
from Portal import settings

from django.contrib.auth.models import User
from Portal.hvp.models.users.UserProfile import UserProfile
from Portal.hvp.models.users.UserInstitution import UserInstitution

def admin_user_management_view(request):
    if request.user.is_authenticated():
        access = False
        isAdmin = False

        profile = request.user.get_profile();
        if profile.IsHVPAdmin:
            access = True
            isAdmin = True
        elif profile.IsLabLeader:
            access = True
            isAdmin = False

        if access == True:
            if request.method == "POST":
                userID = request.POST['userID']
                action = request.POST['action']
                setValue = request.POST['action_value']

                handleAction(isAdmin, userID, action, setValue)

            if isAdmin == True:
                userlist = User.objects.filter(userprofile__AccessStatus=2)
            else:
                userlist = User.objects.filter(userprofile__AccessStatus=2).filter(CurrentInstitution=request.user.CurrentInstitution)

            return render_to_response('users/admin_user_management.html', 
                {
                    'isAdmin': isAdmin,
                    'user': request.user,
                    'userlist': userlist
                })
        else:
            raise Http404("You're no admin!!! You should not be here!")
    else:
        return render_to_response('home/timeout.html')

# To set checkboxes
def handleAction(isAdmin, userID, action, setValue):
        setUser = get_object_or_404(User, pk=userID)
        value = False
        if setValue == "true":
            value = True
        user_profile = setUser.get_profile()

        if action == "hvpadmin" and isAdmin == True:
            user_profile.IsHVPAdmin = value
            user_profile.save()
        elif action == "lableader":
            user_profile.IsLabLeader = value
            user_profile.save()
        elif action == "active":
            setUser.is_active = value
            setUser.save()
        else:
            raise Http404("Invalid action")



