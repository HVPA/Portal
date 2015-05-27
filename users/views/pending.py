################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 515 $
# Last Modified: $Date: 2011-06-29 12:37:18 +1000 (Wed, 29 Jun 2011) $ 
#
# === Description ===
#
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext
from Portal import settings

from django.db.models import Q
from django.contrib.auth.models import User
from Portal.hvp.models.users.UserProfile import UserProfile
from Portal.hvp.models.users.UserInstitution import UserInstitution

def pending_view(request):
    if request.user.is_authenticated():
        if request.user.get_profile().IsHVPAdmin == True:
            # 1 = pending
            # 3 = further clarification
            # 5 = change org

            pending_list = User.objects.filter(
                Q(userprofile__AccessStatus=1)|
                Q(userprofile__AccessStatus=3)|
                Q(userprofile__AccessStatus=5))

            return render_to_response('users/pending.html',
                {
                    #'debug': True,
                    #'debug_message': dir(pending_list),
                    'user': request.user,
                    'pending_list': pending_list,
                })
        else:
            return render_to_response('home/permission.html', {'user': request.user})
    else:
        return render_to_response('home/timeout.html')

