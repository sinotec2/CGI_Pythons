#!/opt/anaconda3/envs/py27/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb; cgitb.enable()
import tempfile as tf
import subprocess
from pykml import parser
from rd_kmlLL import rd_kmlLL
from pyproj import Proj
import twd97
from pandas import *

form = cgi.FieldStorage()


mmif_parm=['AER_MIN_OBUK', 'POINT', 'AER_LAYERS', 'AER_MIN_MIXHT', 'INPUT', 'GRID', 'TIMEZONE', 'PBL_RECALC', 'AER_MIN_SPEED', 'OUTPUT', 'STOP', 'FSL_INTERVAL', 'LAYERS', 'STABILITY', 'START']
mmif_parm=set(mmif_parm)
ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
# 獲取檔名
fileitem = form['filename']
year = form.getvalue('year')
yy=year[2:]
year = int(year)
MMIF='/opt/local/bin/mmif'
WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
pth=WEB+'isc_results/mmif_'+ran+'/'
OUT='>> '+pth+'isc.out'
SED='/usr/bin/sed -ie'
os.system('mkdir -p '+pth)
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)



# 檢測檔案是否上傳
r=1
if fileitem.filename:
  # 設定檔案路徑 
  fn = os.path.basename(fileitem.filename)
  open(pth+fn, 'wb').write(fileitem.file.read())  
  if 'kml' in fn:
    nplgs,npnts,nms,hgts,lon,lat,lonp,latp=rd_kmlLL(pth+fn)    
    s=''
    for n in nms[nplgs:]:
      n+=s
    case=s[:8]
    lon,lat=lon[0],latp[0]
    print case+(' {:f} {:f} </body></html>').format(lat,lon)
    if yy != '20' :
      print '<p>Only 2020 wrf can be re-run in iMac, your request year=20'+yy+'</p>'
    cmd ='cd '+pth+';'
    cmd+='cp ../mmif.inp_blank20 mmif.inp;'
    cmd+=SED+' "s/LATI/{:f}/g" mmif.inp'.format(lat)+';'
    cmd+=SED+' "s/LONG/{:f}/g" mmif.inp'.format(lon)+';'
    cmd+=SED+' "s/xiehe/{:s}/g" mmif.inp'.format(case)
    os.system('echo "'+cmd+'"'+OUT)
    os.system(cmd)
  sfc=subprocess.check_output('grep " sfc " '+pth+'mmif.inp|awk "{print \$NF}"',shell=True).decode('utf8').strip('\n').strip('\r')
  ext=sfc.split('.')[-1]
  case=sfc.replace(ext,'')
  orig=pnyc(lon,lat, inverse=False)
  IJ=(int(orig[0]/3000)+int(83/2))*1000+(int(orig[1]/3000)+int(137/2))
  dfname=WEB+'mmif_results/TWN_3X3_mmif.csv'
  df=read_csv(dfname)
  run_mmif=False
  if IJ in list(df.IJ) and year in set(list(df.YR)):
    boo=(df.IJ==IJ) &(df.YR==year)
    caseold=list(df.loc[boo,'FNAME'])[0]
    os.system('cp '+caseold+'.sfc '+pth+case+'sfc')
    os.system('cp '+caseold+'.pfl '+pth+case+'pfl')
  else:
    if yy=='20':
      cmd ='cd '+pth+';'
      cmd+=MMIF+'|grep Hourly|grep written>'+case+'out &disown'
      os.system('echo "'+cmd+'"'+OUT)
      r=os.system(cmd)
      run_mmif=True
    else:
      print 'mmif needs 20'+yy+' WRF data!</body></html>'
      sys.stdout.close()
      sys.exit('lack of data!')
if not os.path.exists(pth+case+'sfc') or not os.path.exists(pth+case+'pfl'):
  if r!=0:
    ename=pth+case+'out'	
    print """Something wrong in MMIF excutions, see <a data-auto-download href="%s">%s</a>
    </body></html>
    """  % (ename.replace(WEB,'../../../'),ename.split('/')[-1])
    sys.exit()

if run_mmif:  
  pid=subprocess.check_output('ps -ef|grep aermod|head -n1|/opt/local/bin/awkk 2',shell=True).decode('utf8').strip('\n')
  if len(pid)>0:
    print 'mmif is running at pid= '+pid+'</br>'
    print """\
      MMIF_results: The MMIF process will take hours. You may check them during program excution:</br>
      DO NOT RELOAD this web-page !!!</br>
      """
    os.system('sleep 30s')  
  else:
    print """Something wrong in MMIF excutions!"""
    sys.exit('mmif not run')
fnames=subprocess.check_output('ls '+pth,shell=True).decode('utf8').strip('\n').split()
for fn in fnames:
  fname=pth+fn
  print """\
  <a data-auto-download href="%s">%s</a></br>
  """  % (fname.replace(WEB,'../../../'),fname.split('/')[-1])
print '</body></html>'
sys.stdout.close()
sys.exit('fine!')
