
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 650 $
# Last Modified: $Date: 2013-08-08 14:30:15 +1400 (Thu, 8 Aug 2013) $ 
#
# === Description ===
#
#
################################################################################

from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from Portal.hvp.models.users.UserProfile import UserProfile
from Portal import settings
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

# sends an email from the portal admin email account
def admin_email_view(request):
    # kick user if not authenticated or they are not an admin
    if not request.user.is_authenticated() or not request.user.get_profile().IsHVPAdmin:
        return render_to_response('home/timeout.html')
    
    # init vars
    subject, recipient, recipient_stripped, message, sent = '', '', '', '', ''
    error_msg, error = '', False
    
    # send email
    try:
        if request.POST:
            subject = request.POST['subject']
            message = request.POST['message']
            recipient = request.POST['recipient'].split(' ')
            
            # print the email addresses from tuple
            for r in recipient:
                recipient_stripped += r + ' '
            
            send_mail(  request.POST['subject'],
                        request.POST['message'],
                        settings.ADMIN_EMAIL,
                        recipient,
                        fail_silently = False)
            
            sent = recipient_stripped
            subject, message, recipient_stripped = '', '', ''
    except Exception as ex: 
        error = True
        # log: could not send email
        logger.error('Send Test Email failed to ' + recipient_stripped + ': ' + str(ex))
    

    return render_to_response('users/admin_email.html', {   'user': request.user, 
                                                            'sender': settings.ADMIN_EMAIL, 
                                                            'subject': subject,
                                                            'message': message,
                                                            'sent': sent,
                                                            'error': error,
                                                            'error_msg': error_msg,
                                                            'recipient': recipient_stripped.replace("'","")})
                                                            
