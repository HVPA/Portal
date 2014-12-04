#!/usr/bin/python

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


import subprocess

subprocess.call('python -m smtpd -n -c DebuggingServer localhost:1025',shell=True)
