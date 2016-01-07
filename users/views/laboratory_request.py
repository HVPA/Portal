from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.models import User
from Portal.hvp.models.users.LabRequest import LabRequest
from Portal.hvp.models.users.UserProfile import UserProfile
from Portal.hvp.models.ref.RefLabRequestStatus import RefLabRequestStatus
from Portal.hvp.models.labs.LabDetail import LabDetail
from Portal.hvp.models.labs.LabContact import LabContact
from django.core.mail import send_mail
from Portal import settings
import datetime
import logging

logger = logging.getLogger(__name__)

# admin management page contains all the requests from users
def admin_laboratory_request_view(request):
    if request.user.is_authenticated():
        if request.user.get_profile().IsHVPAdmin:
            # get all the lab requests
            lab_requests = LabRequest.objects.all()
            
            return render_to_response('users/admin_laboratory_request.html',
                                      {
                                          "lab_requests": lab_requests,
                                          "user": request.user,
                                      })
            
        else:
            raise Http404("You're no admin!!! You should not be here")
    else:
        return render_to_response('home/timeout.html')

# admin views a single request from user, here they can grant or deny their request
def admin_laboratory_request_page_view(request, labRequestID):
    if request.user.is_authenticated():
        if request.user.get_profile().IsHVPAdmin:
            # init error
            error = ''
            
            # get the lab request
            lab_request = LabRequest.objects.get(pk=labRequestID)

            # get org id to query external db
            org_id = lab_request.VariantInstance.Organisation.HashCode

            # get lab and contact information
            ##lab_details = LabDetail.objects.using('labs').get(Org_Hash=org_id)
            ##lab_contacts = LabContact.objects.using('labs').filter(Lab=lab_details)
            lab_details = LabDetail.objects.get(Org_Hash=org_id)
            lab_contacts = LabContact.objects.filter(Lab=lab_details)
            
            # if admin grants user lab details
            if 'grant' in request.POST:
                # set the lab request and date
                lab_request.LabRequestStatus = RefLabRequestStatus.objects.get(pk=2)
                lab_request.StatusDateUpdated = datetime.date.today()
                lab_request.save()

                # send out email
                error = send_lab_details_email(lab_request, lab_details, lab_contacts)
                
                if not error:
                    return HttpResponseRedirect('/request/')

            # if admin denys you lab details
            if 'reject' in request.POST:
                # set the lab request and date
                lab_request.LabRequestStatus = RefLabRequestStatus.objects.get(pk=3)
                lab_request.StatusDateUpdated = datetime.date.today()
                lab_request.save()

                # send out email
                error = send_rejected_request_email(lab_request)
                
                if not error:
                    return HttpResponseRedirect('/request/')

            return render_to_response('users/admin_laboratory_request_page.html',
                                      {
                                          "user": request.user,
                                          "lab_request": lab_request,
                                          "lab_details": lab_details,
                                          "lab_contacts": lab_contacts,
                                          "error": error,
                                      })
            
        else:
            raise Http404("You're no admin!!! You should not be here")
    else:
        return render_to_response('home/timeout.html')

# user management page that allows user to view all current request they have made
def user_laboratory_request_view(request):
    if request.user.is_authenticated():
        # get all user lab request
        lab_request = LabRequest.objects.filter(User=request.user)

        return render_to_response('users/user_laboratory_request.html',
                                  {
                                      "user": request.user,
                                      "lab_requests": lab_requests,
                                  })
    else:
        return render_to_response('home/timeout.html')


# user views a single request they made.
def user_laboratory_request_page_view(request, labRequestID):
    if request.user.is_authenticated():

        return render_to_response('users/user_laboratory_request_page.html')
    else:
        return render_to_response('home/timeout.html')

# sends an email to user with the contact details to the lab the requested
def send_lab_details_email(lab_request, lab_details, lab_contacts):    
    error = ''
    fromEmail = settings.ADMIN_EMAIL
    toEmail = lab_request.User.email
    
    try:
        send_mail(
            '[HVP]Your Lab Request has been granted', # subject
            (
                'Dear ' + lab_request.User.first_name + ' ' + lab_request.User.last_name + ',\n' +
                '\nYour request for lab contact details made on the ' + str(lab_request.ApplicationDate) +
                ', has been granted. Below are the contact information of the lab you have requested for:\n\n' +
                'Lab: \n' +
                lab_details.Org_Name + '\n' +
                lab_details.Lab_Name + '\n' +
                lab_details.Address_1 + '\n' +
                str(lab_details.Address_2) + '\n' +
                lab_details.City + ', ' + lab_details.Post + ', ' +
                lab_details.State.State + '\n\n' +
                'Contact Details: ' +
                display_contact_details(lab_contacts) +
                '\nRegards.\n\nHVP Australia'
            ),
            fromEmail,
            [toEmail],
            fail_silently = False
            )
    except Exception as ex:
        # log: could not send email to user
        logger.error('Lab access email could not be sent to ' + toEmail + ': ' + str(ex))
        error = 'Email to user: ' + toEmail + ' for Lab Request Granted could not be sent. Please try again later, if that still fails click <a href="mailto:' + toEmail + '?Subject=[HVP]%20Lab%20Request%20Granted">here</a> to send an email to them directly. Sorry for the inconvenience.'
        
    return error
    
    
# iterates throught the list of lab contacts and display them in an ordered structured way.
def display_contact_details(lab_contacts):
    display = ''

    for contact in lab_contacts:
        display = (
            display + '\n' +
            contact.Title.Title + ' ' + contact.First_Name + ' ' + contact.Last_Name + '\n' +
            'Phone: ' + contact.Phone + '\n' +
            'Mobile: ' + str(contact.Mobile) + '\n' +
            'Fax: ' + str(contact.Fax) + '\n' +
            'Email: ' + contact.Email + '\n' 
        )
    
    return display

# sends an email rejection to user that their request has been denied
def send_rejected_request_email(lab_request):
    error = ''
    fromEmail = settings.ADMIN_EMAIL
    toEmail = lab_request.User.email
    
    try:
        send_mail(
            '[HVP]Your Lab Request has been rejected', # subject
            (
                'Dear ' + lab_request.User.first_name + ' ' + lab_request.User.last_name + ',\n' +
                '\nYour request for lab contact details made on the ' + str(lab_request.ApplicationDate) +
                ', has been rejected.' + '\n\nRegards.\n\nHVP Australia'
             ),
            fromEmail,
            [toEmail],
            fail_silently = False
            )
    except Exception as ex:
        # log: could not send email to user
        logger.error('Lab rejection email could not be sent to ' + toEmail + ': ' + str(ex))
        error = 'Email to user: ' + toEmail + ' for Lab Request Rejected could not be sent. Please try again later, if that still fails click <a href="mailto:' + toEmail + '?Subject=[HVP]%20Lab%20Request%20Rejected">here</a> to send an email to them directly. Sorry for the inconvenience.'
    
    return error
    
    
