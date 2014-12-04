################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 623 $
# Last Modified: $Date: 2013-07-04 18:09:07 +1000 (Thu, 04 Jul 2013) $ 
#
# === Description ===
#
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from Portal.hvp.models.users.UserInstitution import UserInstitution
from Portal.hvp.models.users.InstitutionContact import InstitutionContact
from Portal.hvp.models.users.UserProfile import UserProfile
from Portal.hvp.models.users.LaboratoryGroup import LaboratoryGroup
from Portal.hvp.models import ref

def test_view(request):
    return render_to_response('users/tests.html')

def user_account_view(request):
    if request.user.is_authenticated():
        # get all ref data
        title_list = ref.RefTitle.objects.all()
        state_list = ref.RefState.objects.all()
        usage_list = ref.RefUsageIntention.objects.all()
        
        # init password errors/messages
        old_password_error = False # error when change password and old password was incorrect
        confirm_password_error = False # error when new password is different when typed in the confirm
        password_changed = False # message when password has been successfully changed
        saved_changes = False # message when user details have been saved successfully
        request_org_change = False # disables request org change button display message to user
        assigned_org = False # use for alerting user they have been assigned to org or not
        
        # get all the user related data
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        """
        try:
            current_institution = user.CurrentInstitution
        except:
            current_institution = None
        current_contact = None
        if current_institution != None:
            current_contact = get_object_or_404(InstitutionContact, UserInstitution=current_institution)
            
        try:
            pending_institution = user.PendingInstitution
        except:
            pending_institution = None
        pending_contact = None
        if pending_institution != None:
            pending_contact = get_object_or_404(InstitutionContact, UserInstitution=pending_institution)
            request_org_change = True
        """
        try:
            institution = user.Institution
        except:
            institution = None
            contact = None
        if institution != None:
            contact = get_object_or_404(InstitutionContact, UserInstitution=institution)
        
        # change password
        if 'password' in request.POST:
            # validate old password
            if user.check_password(request.POST['old_password']):
                # check if new password matches with new confirm password 
                if request.POST['new_password'] == request.POST['confirm_new_password']:
                    # save the new password
                    #TODO: send out new password to user email
                    user.set_password(request.POST['new_password'])
                    user.save()
                    
                    # password change message
                    password_changed = True
                else:
                    # confirm password error
                    confirm_password_error = True
            else:
                # old password error
                old_password_error = True
        
        # changing organisation
        #if 'change_org' in request.POST:
        #    return HttpResponseRedirect('/user/change_org/')
        
        # updating user data
        if 'update' in request.POST:
            # update user details
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email = request.POST['user_email']
            user.username = request.POST['user_email']
            
            # update user profile details
            user_profile.user = user
            user_profile.Phone = request.POST['user_phone']
            user_profile.Mobile = request.POST['user_mobile']
            
            # try and get user title
            user_title = request.POST['user_title']
            if (user_title):
                user_profile.Title = ref.RefTitle.objects.get(Title__iexact = user_title)

            # institution
            institution.Name = request.POST['org_name']
            institution.Department = request.POST['org_dept']
            institution.Address = request.POST['org_address']
            institution.City = request.POST['org_city']
            inst_state = request.POST['org_state']
            if inst_state:
                institution.State = ref.RefState.objects.get(State__iexact = inst_state)
            institution.PostCode = request.POST['org_post']
            institution.Phone = request.POST['org_phone']
            institution.Fax = request.POST['org_fax']
            
            # contact
            contact_title = request.POST['contact_title']
            if contact_title:
                contact.ContactTitle = ref.RefTitle.objects.get(Title__iexact = contact_title)
            contact.ContactFirstName = request.POST['contact_firstname']
            contact.ContactLastName = request.POST['contact_lastname']
            contact.ContactPhone = request.POST['contact_phone']
            contact.ContactEmail = request.POST['contact_email']
            
            # saved message
            saved_changes = True
            
            # save objects
            user.save()
            user_profile.save()
            institution.save()
            contact.save()
        
        return render_to_response('users/user_account.html',
                                  {
                                   'title_list': title_list,
                                   'state_list': state_list,
                                   'usage_list': usage_list,
                                   'password_changed': password_changed,
                                   'old_password_error': old_password_error,
                                   'confirm_password_error': confirm_password_error,
                                   'saved_changes': saved_changes,
                                   'request_org_change': request_org_change,
                                   'assigned_org': assigned_org,
                                   'user': user,
                                   'institution': institution,
                                   'contact': contact,
                                   #'current_institution': current_institution,
                                   #'current_contact': current_contact,
                                   #'pending_institution': pending_institution,
                                   #'pending_contact': pending_contact,
                                   'debug': False,
                                   #'debug_message': dir(current_contact)
                                   })
    else:
        return render_to_response('home/timeout.html')
