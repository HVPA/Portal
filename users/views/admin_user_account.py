################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 656 $
# Last Modified: $Date: 2013-08-13 16:41:52 +1000 (Tue, 13 Aug 2013) $ 
#
# === Description ===
#
#
################################################################################

from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from Portal.hvp.models.users.UserProfile import UserProfile
from Portal.hvp.models.users.UserInstitution import UserInstitution
from Portal.hvp.models.users.InstitutionContact import InstitutionContact
from Portal.hvp.models.users.UserDocument import UserDocument 
from Portal.hvp.models import ref
from django.http import Http404
import datetime
from Portal.users.UploadFileForm import UploadFileForm

from django.contrib.auth.decorators import login_required
import os, mimetypes
from django.contrib import auth

from django.core.mail import send_mail
from Portal import settings
import logging

logger = logging.getLogger(__name__)

def reset_password():
    return User.objects.make_random_password(length=10, 
        allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')

def grant_application(user_obj, user_profile):
    # set user profile access status: approved/granted
    user_profile.AccessStatus = get_object_or_404(ref.RefAccessStatus, pk=2)
    user_profile.AccessGrantedDate = datetime.date.today()
    user_profile.save()
    
    # set user is active
    user_obj.is_active = True
    user_obj.save()
    
    # send email
    return send_grant_email(user_obj, user_profile)

def request_clarification(user_obj, user_profile):
    # set user profile access status: pending approval
    user_profile.AccessStatus = get_object_or_404(ref.RefAccessStatus, pk=1)
    user_profile.save()
    
    # set user is not active
    user_obj.is_active = False
    user_obj.save()

    # send email
    return send_clarification_email(user_obj, user_profile)
    
def reject_application(user_obj, user_profile):    
    # set userprofile access status: rejected
    user_profile.AccessStatus = get_object_or_404(ref.RefAccessStatus, pk=4)
    user_profile.save()
    
    # set user is not active
    user_obj.is_active = False
    user_obj.save()
    
    # send email
    return send_rejection_email(user_obj, user_profile)

    
def send_password_reset_email(user_obj, user_profile, password):
    error = ''
    try:
        send_mail(
            'HVP Australia - Your password has been reset',
            'Dear ' + user_profile.Title.Title + ' ' + user_obj.first_name + ' ' + user_obj.last_name + ',\nYour password has been reset to: ' + password,
            settings.ADMIN_EMAIL,
            [user_obj.email],
            fail_silently=False)
    except Exception as ex:
        # log: could not send email to user
        logger.error('User password reset email failed to be sent to ' + user_obj.email + ': ' + str(ex))
        error = 'Email to user: ' + user_obj.email + ' for password reset could not be sent. Please try again later, if that still fails click <a href="mailto:' + user_obj.email + '?Subject=[HVP]%20Password Reset&Body=Your new password is: ' + password + '">here</a> to send an email to them directly. Sorry for the inconvenience.'
        
    return error
    
    
def send_grant_email(user_obj, user_profile):
    error = ''
    try:
        send_mail(
            'HVP Australia - Your account access has been approved',
            'Dear ' + user_profile.Title.Title + ' ' + user_obj.first_name + ' ' + user_obj.last_name + ',\nWelcome to the Human Variome Project Portal, to start using the Portal please sign in at ' + settings.PORTAL_URL, 
            settings.ADMIN_EMAIL,
            [user_obj.email],
            fail_silently=False)
    except Exception as ex:
        # log: could not send email to user
        logger.error('User access approval email failed to be sent to ' + user_obj.email + ': ' + str(ex))
        error = 'Email to user: ' + user_obj.email + ' for access approval could not be sent. Please try again later, if that still fails click <a href="mailto:' + user_obj.email + '?Subject=[HVP]%20Access%20granted">here</a> to send an email to them directly. Sorry for the inconvenience.'
        
    return error
    
    
def send_clarification_email(user_obj, user_profile):
    error = ''
    try:
        send_mail(
                  'HVP Australia - You are required to clairfy your details',
                  'Dear ' + user_profile.Title.Title + ' ' + user_obj.first_name + ' ' + user_obj.last_name + 
                  ',\nYou need to clarify your creditials, to ensure that HVP Usage Policies are met we require additional info to verify your eligibility to access this site. \nPlease sign in at  ' + settings.PORTAL_URL +
                  ' and resubmit your details.',
                  settings.ADMIN_EMAIL,
                  [user_obj.email],
                  fail_silently=False
                  )
    except Exception as ex:
        # log: could not send email to user
        logger.error('User clarification email failed to be sent to ' + user_obj.email + ': ' + str(ex))
        error = 'Email to user: ' + user_obj.email + ' for clarification could not be sent. Please try again later, if that still fails click <a href="mailto:' + user_obj.email + '?Subject=[HVP]%20Clarification%20required">here</a> to send an email to them directly. Sorry for the inconvenience.'
        
    return error

def send_rejection_email(user_obj, user_profile):
    error = ''
    try:
        send_mail(
                  'HVP Australia - Your application has been rejected',
                  'Dear ' + user_profile.Title.Title + ' ' + user_obj.first_name + ' ' + user_obj.last_name + ',\nIt is unfortunate but we must inform you that your application has been rejected.',
                  settings.ADMIN_EMAIL,
                  [user_obj.email],
                  fail_silently=False
                  )
    except Exception as ex:
        # log: could not send email to user
        logger.error('User rejection email failed to be sent to ' + user_obj.email + ': ' + str(ex))
        error = 'Email to user: ' + user_obj.email + ' for access rejected could not be sent. Please try again later, if that still fails click <a href="mailto:' + user_obj.email + '?Subject=[HVP]%20Access%20Rejected">here</a> to send an email to them directly. Sorry for the inconvenience.'
    
    return error
    
    
# Following store paths for different kinds of access based files
# For example, all users (authenticated or anonymous) are able to
# download files in unrestricted directory
RESTRICTED_DOWNLOAD_PATH = '/Users/mel/projects/HVP/trunk/Portal/source/Portal/uploads/'

def sendfile(filewithpath, filename):
    """It will get filename and filename with full path, prepare an
    HttpResponse with headers, and return it
    This function was inspired by and copied from
    http://revjohnnyhealey.wordpress.com/2009/09/10/djangocon-x-sendfile-lightning-talk/
    This is *not* a view. It's a helper function.

    """
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse('', content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['X-Sendfile'] = filename
    response['Content-Disposition'] = "attachment; filename=%s" % (filewithpath)
    return response

def downloadfile(request, userID):
    """This is a Django view which gets the name of the file to download
    It then decides, based on user's authenticated status and file location
    whether the user can download file or not

    """
    user_obj = get_object_or_404(User, pk=userID)
    user_doc = get_object_or_404(UserDocument, user = user_obj)
#    name = str(user_doc.file).split('/')
#    filename = name[1]
    
    filename = '41_PARTS.pdf'
    
    restricted_filetodownload = ''.join([RESTRICTED_DOWNLOAD_PATH, filename])
    
    if request.user.is_authenticated():
        # Access to unrestricted and login
        # TO DO: restricted
        if request.user.get_profile().IsHVPAdmin:
            return sendfile(filename, restricted_filetodownload)
        else:
            # TO DO: restricted
            raise Http404('Not admin')


def admin_user_account_view(request, userID):
    if request.user.is_authenticated():
        if request.user.get_profile().IsHVPAdmin:    
            # get all ref data
            title_list = ref.RefTitle.objects.all()
            state_list = ref.RefState.objects.all()
            usage_list = ref.RefUsageIntention.objects.all()
            
            # init errors/messages
            saved_user_changes = False
            saved_inst_changes = False
            new_password = None
            status_changed = False
            launch_inst_tab = False
            # email error
            error = ''
            
            # get all the user_obj related data
            # user_obj is the user_obj the admin is viewing
            user_obj = get_object_or_404(User, pk=userID)
            user_profile = get_object_or_404(UserProfile, user=user_obj)
            
            try:
                institution = user_obj.Institution
            except:
                institution = None
            contact = None
            if institution != None:
                contact = get_object_or_404(InstitutionContact, UserInstitution=institution)
                
            # reset password
            if 'reset_password' in request.POST:
                new_password = reset_password()
                user_obj.set_password(new_password)
                user_obj.save()
                
                # send password
                error = send_password_reset_email(user_obj, user_profile, new_password)
            
            # set user_obj status
            if 'grant' in request.POST:
                error = grant_application(user_obj, user_profile)
            if 'request' in request.POST:
                error = request_clarification(user_obj, user_profile)
            if 'reject' in request.POST:
                error = reject_application(user_obj, user_profile)
            
            if 'update_user' in request.POST or 'update_inst' in request.POST:
            
                # save any changes made to user_obj details
                # user_obj
                user_obj.first_name = request.POST['firstname']
                user_obj.last_name = request.POST['lastname']
                user_obj.email = request.POST['user_email']
                
                # user_profile
                user_profile.Phone = request.POST['user_phone']
                user_profile.Mobile = request.POST['user_mobile']
                
                # try and get ref data to save
                user_title = request.POST['user_title']
                usage = request.POST['usage']
                if (user_title):
                    user_profile.Title = ref.RefTitle.objects.get(Title__iexact = user_title)
                if (usage):
                    user_profile.UsageIntention = ref.RefUsageIntention.objects.get(UsageIntention__iexact = usage)
                
                # save user details
                user_obj.save()
                user_profile.save()
                
                # user_institution
                institution.Name = request.POST['inst_name']
                institution.Department = request.POST['inst_dept']
                institution.Address = request.POST['inst_address']
                institution.City = request.POST['inst_city']
                institution.PostCode = request.POST['inst_post']
                institution.Phone = request.POST['inst_phone']
                institution.Fax = request.POST['inst_fax']
                
                # pending contact
                contact.ContactFirstName = request.POST['contact_firstname']
                contact.ContactLastName = request.POST['contact_lastname']
                contact.ContactPhone = request.POST['contact_phone']
                contact.ContactEmail = request.POST['contact_email']
                
                # try and get ref data to save
                inst_state = request.POST['inst_state']
                if (inst_state):
                    institution.State = ref.RefState.objects.get(State__iexact = inst_state)
                    
                contact_title = request.POST['contact_title']
                if (contact_title):
                    contact.ContactTitle = ref.RefTitle.objects.get(Title__iexact = contact_title)
                
                # save institution details
                institution.save()
                contact.save()
                
                
                # sets the institution tab to be the selected on page load
                if 'update_inst' in request.POST:
                    launch_inst_tab = True
                
                # save message
                saved_inst_changes = True
                saved_user_changes = True
            
            return render_to_response('users/admin_user_account.html',
                                      {
                                       'user': request.user,
                                       #'user_doc': user_doc,
                                       'title_list': title_list,
                                       'state_list': state_list,
                                       'usage_list': usage_list,
                                       'saved_user_changes': saved_user_changes,
                                       'saved_inst_changes': saved_inst_changes,
                                       'new_password': new_password,
                                       'status_changed': status_changed,
                                       'user_obj': user_obj,
                                       'institution': institution,
                                       'contact': contact,
                                       'launch_inst_tab': launch_inst_tab,
                                       'debug': False,
                                       'error': error,
                                       #'debug_message': dir(current_contact)
                                       })
        else:
            raise Http404("You're no admin!!! You should not be here!")
    else:
        return render_to_response('home/timeout.html')
