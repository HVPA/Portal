################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 816 $
# Last Modified: $Date: 2014-04-16 15:33:59 +1000 (Wed, 16 Apr 2014) $ 
#
# === Description ===
#
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from Portal.hvp.models.users.UserProfile import UserProfile
from Portal.hvp.models.users.UserInstitution import UserInstitution
from Portal.hvp.models.users.InstitutionContact import InstitutionContact
from Portal.hvp.models.users.UserDocument import UserDocument
from Portal.hvp.models import ref
from django.http import Http404
# from Portal.users.UploadFileForm import UploadFileForm
from django.core.mail import send_mail
from Portal import settings
from datetime import date
import logging

logger = logging.getLogger(__name__)

# check the file extension is valid
def valid_file_extensions(file_name):
    str_split = file_name.split('.')
    extension = str_split[1]
    
    # valid extensions to check against
    valid_expressions = ['doc', 'docx', 'pdf']
    
    if extension.lower() in valid_expressions:
        return True
    else:
        return False

def signup_view(request):
    # load ref data
    title_list = ref.RefTitle.objects.all()
    state_list = ref.RefState.objects.all()
    usage_list = ref.RefUsageIntention.objects.all()
    
    # init var
    firstName = ''; lastName = ''; username = ''; user_email = ''; password = ''; confirm = ''; user_phone = '';
    user_mobile = ''; user_title = ''; usage = ''; org_name = ''; org_address = ''; org_city = ''; org_dept = '';
    org_state = ''; org_post = ''; org_phone = ''; org_fax = ''; contact_title = ''; contact_firstname = '';
    contact_lastname = ''; contact_phone = ''; contact_email = '';
    
    # init password_error and email_exist bools for validating
    # password and email.
    password_error = False
    email_exist = False
    upload_format_error = False
    username_exist = False
    
    # init form
    #form = UploadFileForm()
    if (request.POST):
        # get user entered details
        # user details
        firstName = request.POST['firstname']
        lastName = request.POST['lastname']
        username = request.POST['username']
        user_email = request.POST['user_email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        user_phone = request.POST['user_phone']
        user_mobile = request.POST['user_mobile']
        user_title = request.POST['user_title']
        usage = request.POST['usage']
        
        # organisation
        org_name = request.POST['org_name']
        org_dept = request.POST['org_dept']
        org_address = request.POST['org_address']
        org_city = request.POST['org_city']
        org_state = request.POST['org_state']
        org_post = request.POST['org_post']
        org_phone = request.POST['org_phone']
        org_fax = request.POST['org_fax']
        contact_title = request.POST['contact_title']
        contact_firstname = request.POST['contact_firstname']
        contact_lastname = request.POST['contact_lastname']
        contact_phone = request.POST['contact_phone']
        contact_email = request.POST['contact_email']
        
        # validate password, email and username
        if bool(password != confirm): 
            password_error = True
        if bool(User.objects.filter(email__iexact=user_email)):
            email_exist = True
        if bool(User.objects.filter(username__iexact=username)):
            username_exist = True
        
        # validate file upload extension
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            if not valid_file_extensions(uploaded_file.name):
                upload_format_error = True
        
        # I know this is stupid but I can't get the 'or' to work
        # for some reason it won't let me do this: if not password_error and not email_exist:
        if not password_error: 
            if not email_exist: 
                if not username_exist:
                    if not upload_format_error:
                        # create user model objects
                        user = User()
                        user_profile = UserProfile()
                        user_institution = UserInstitution()
                        contact = InstitutionContact()
                        
                        try:
                            # save user basic details - password will be encrypted
                            # email will be used as the users username
                            user.username = username
                            user.email = user_email
                            user.first_name = firstName
                            user.last_name = lastName
                            user.set_password(password)
                            user.is_staff = False
                            user.is_active = False
                            user.is_superuser = False

                            # need to save user first before we can assign it to the UserProfile and UserInstitution
                            user.save()

                            # create a user profile
                            user_profile.user = user
                            user_profile.Phone = user_phone
                            user_profile.Mobile = user_mobile
                            user_profile.IsHVPAdmin = False
                            user_profile.IsLabLeader = False

                            # set access level and status
                            user_profile.AccessStatus = get_object_or_404(ref.RefAccessStatus, pk=1)

                            # try and get ref to save
                            if (user_title):
                                user_profile.Title = ref.RefTitle.objects.get(Title__iexact = user_title)
                            if (usage):
                                user_profile.UsageIntention = ref.RefUsageIntention.objects.get(UsageIntention__iexact = usage)     

                            user_profile.save()


                            # create UserInstitution
                            user_institution.User = user
                            user_institution.PendingInstitution = user;
                            user_institution.BelongsTo = user;
                            user_institution.Institution = user;

                            user_institution.Name = org_name
                            user_institution.Department = org_dept
                            user_institution.Address = org_address
                            user_institution.City = org_city
                            if (org_state):
                                user_institution.State = ref.RefState.objects.get(State__iexact = org_state)
                            user_institution.PostCode = org_post
                            user_institution.Phone = org_phone
                            user_institution.Fax = org_fax

                            user_institution.ApplicationDate = date.today()

                            user_institution.save()


                            # try and get ref to save
                            if (contact_title):
                                contact.ContactTitle = ref.RefTitle.objects.get(Title__iexact = contact_title)                        
                            contact.ContactFirstName = contact_firstname
                            contact.ContactLastName = contact_lastname
                            contact.ContactPhone = contact_phone
                            contact.ContactEmail = contact_email

                            contact.UserInstitution = user_institution

                            contact.save()
                            
                            # send email
                            send_new_signup_email(user)
                                
                            """
                            # file upload
                            if uploaded_file:
                                uploaded_file.name = str(user.id) + '_' + uploaded_file.name
                                form = UploadFileForm(request.POST, request.FILES)
                                form.save()

                                # add the user fk to upload
                                filename = 'uploads/' + uploaded_file.name
                                upload = UserDocument.objects.get(file = filename)
                                upload.user = user
                                upload.save()
                            """
                            
                        except:
                            # in case of error! we delete objects if they have an id, the id
                            # will mean the object was saved with an auto incremented id.
                            # We use delete as there is no rollback feature in django :(
                            if user.id != None:
                                user.delete()
                            if user_profile.id != None:
                                user_profile.delete()
                            if user_institution.id != None:
                                user_institution.delete()
                            if contact.id != None:
                                contact.delete()
                            # TODO: if signup failed and user uploaded a file need to delete the
                            # file from the 'uploads/' directory and removed the record from 
                            # UserDocument table.  
                            
                            raise Http404('Something has gone horribly wrong! Please try again or contact the HVP system admin.') 
                        
                        return render_to_response('users/signup_complete.html')
        
    return render_to_response('users/signup.html',
                              {
                               #'form': form,
                               'title_list': title_list,
                               'state_list': state_list,
                               'usage_list': usage_list,
                               'password_error': password_error,
                               'email_exist': email_exist,
                               'username_exist': username_exist,
                               'upload_format_error': upload_format_error,
                               'firstName': firstName,
                               'lastName': lastName,
                               'username': username,
                               'user_email': user_email,
                               'user_phone': user_phone,
                               'user_mobile': user_mobile,
                               'user_title': user_title,
                               'usage': usage,
                               'org_name': org_name,
                               'org_dept': org_dept,
                               'org_address': org_address,
                               'org_city': org_city,
                               'org_state': org_state,
                               'org_post': org_post,
                               'org_phone': org_phone,
                               'org_fax': org_fax,
                               'contact_title': contact_title,
                               'contact_firstname': contact_firstname, 
                               'contact_lastname': contact_lastname,
                               'contact_phone': contact_phone,
                               'contact_email': contact_email
                               })

def send_new_signup_email(user):
    # sends an email to the admin email to notify/action a new user needs to be verified 
    try:
        send_mail(
                    '[HVP]New user signup', # subject
                    (
                        'A new user has signed up and is awaiting approval' +
                        '\n' + user.first_name + ' ' + user.last_name +
                        '\n' + user.email
                     ),
                    settings.ADMIN_EMAIL, # sender
                    [settings.ADMIN_EMAIL], # recipient
                    fail_silently = False
                )
    except Exception as ex:
        # log: could not send email to user
        logger.error('Signup email could not be sent to ' + user.email + ': ' + str(ex))
