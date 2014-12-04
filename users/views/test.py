################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: AlanLo $
# Last Revision: $Rev: 218 $
# Last Modified: $Date: 2010-07-27 10:38:46 +1000 (Tue, 27 Jul 2010) $ 
#
# === Description ===
#
#
################################################################################


from django.shortcuts import render_to_response

def test_view(request):
    return render_to_response('users/tests.html')
