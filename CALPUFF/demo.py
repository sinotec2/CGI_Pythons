#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb 
import subprocess

WEB='/Library/WebServer/Documents'
CGI='/Library/WebServer/CGI-Executables/calpuff/'
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
pth=WEB+'/cpuff_results/demo/'
rrn='/cpuff_results/demo/'
#The Resultant File Links
fnames=subprocess.check_output("ls -lh "+pth+"|awk '{print $9}' ",shell=True).decode('utf8').split('\n')
fsizes=subprocess.check_output("ls -lh "+pth+"|awk '{print $5}' ",shell=True).decode('utf8').split('\n')
print """\
  <p>Demo Case Model_results:</br>
  """
for fn in fnames:
  if len(fn)<2:continue
  ifn=fnames.index(fn)
  fname=rrn+fn
  print """\
  <p><a href="%s" target="_blank">%s (%s)</a></br>
  """  % (fname,fn,fsizes[ifn])
print '</body></html>'

