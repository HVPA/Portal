################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: AlanLo $
# Last Revision: $Rev: 226 $
# Last Modified: $Date: 2010-07-27 18:29:59 +1000 (Tue, 27 Jul 2010) $ 
#
# === Description ===
#
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from Portal.hvp.models import ref
from Portal.hvp.models.users.UserInstitution import UserInstitution
from Portal.hvp.models.users.InstitutionContact import InstitutionContact
from Portal.hvp.models.users.UserProfile import UserProfile
import datetime
from django.http import HttpResponseRedirect

# gets date string and returns it as a valid datetime object
def get_date(date_str):
    split = date_str.split('/')
    date = datetime.date(int(split[2]), int(split[1]), int(split[0]))
    return date

def change_org_view(request):
    if request.user.is_authenticated():
        # get all ref data
        title_list = ref.RefTitle.objects.all()
        state_list = ref.RefState.objects.all()
        
        user = request.user
        
        # add new user institution
        if 'change' in request.POST:
            # get all user & user org
            user_profile = get_object_or_404(UserProfile, user = user)
            
            # create a new user institution
            new_user_institution = UserInstitution()
            new_institution_contact = InstitutionContact()
            
            # institution details
            new_user_institution.Name = request.POST['org_name']
            new_user_institution.Department = request.POST['org_dept']
            new_user_institution.Address = request.POST['org_address']
            new_user_institution.City = request.POST['org_city']
            new_user_institution.PostCode = request.POST['org_post']
            new_user_institution.Phone = request.POST['org_phone']
            new_user_institution.Fax = request.POST['org_fax']
            new_user_institution.RequestChange = True
            new_user_institution.StartDate = get_date(request.POST['start_date'])
            if request.POST['end_date'] != '':
                new_user_institution.EndDate = get_date(request.POST['end_date'])
            new_user_institution.ApplicationDate = datetime.date.today()
            
            # set the user it belongs to
            new_user_institution.BelongsTo = user
            
            # set the pending institution
            new_user_institution.PendingInstitution = user
            
            # contact details
            new_institution_contact.ContactFirstName = request.POST['contact_firstname']
            new_institution_contact.ContactLastName = request.POST['contact_lastname']
            new_institution_contact.ContactPhone = request.POST['contact_phone']
            new_institution_contact.ContactEmail = request.POST['contact_email']
            
            # try and get ref data to save
            org_state = request.POST['org_state']
            contact_title = request.POST['contact_title']
            if (org_state):
                new_user_institution.State = ref.RefState.objects.get(State__iexact = org_state)
            if (contact_title):
                new_user_institution.ContactTitle = ref.RefTitle.objects.get(Title__iexact = contact_title)
            
            new_user_institution.save()
            
            # set foreign key relationship
            new_institution_contact.UserInstitution = new_user_institution
            new_institution_contact.save()
            
            # change the access status of the user profile to "Request Change of Organisation"
            # TODO: AccessStatus key will need to be updated
            user_profile.AccessStatus = get_object_or_404(ref.RefAccessStatus, pk=3)
            user_profile.save()
            
            # return user back to the user details page
            return HttpResponseRedirect('/user/')
        
        return render_to_response('users/change_org.html',
                                  {
                                   'title_list': title_list,
                                   'state_list': state_list,
                                   'user': user,
                                   })
    else:
        return render_to_response('home/timeout.html')
