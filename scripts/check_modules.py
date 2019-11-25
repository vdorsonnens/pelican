import sys
import os
import subprocess

res = subprocess.check_output(['pip', 'list'])

if not 'TravisPy' in res:
    os.system("pip install travispy")
if not 'GitPython' in res:
    os.system("pip install gitpython")
