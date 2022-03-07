#!/opt/anaconda3/envs/py27/bin/python
import numpy as np
from pykml import parser
import sys, os
from shapely.algorithms.cga import signed_area
from shapely.geometry import Point, Polygon

def rd_kmlLL(fname):
  kml_file = os.path.join(fname)
  with open(kml_file) as f:
      doc = parser.parse(f).getroot()

#tags for Placemark, Polygon and Point
  plms=doc.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
  try:
    names=[str(i.ExtendedData.Data.value) for i in plms]
  except:
    print ('names must contain building/stack height(m) for objects.')
    sys.exit('names must contain building/stack height(m) for objects.')
  plgs=doc.findall('.//{http://www.opengis.net/kml/2.2}Polygon')
  pnts=doc.findall('.//{http://www.opengis.net/kml/2.2}Point')

  plm_tag=[str(i.xpath).split()[-1][:-2] for i in plms]
  #seq of polygon or point
  plg_prt=[str(i.getparent().values).split()[-1][:-2] for i in plgs]
  pnt_prt=[str(i.getparent().values).split()[-1][:-2] for i in pnts]
  idx_plg=[plm_tag.index(i) for i in plg_prt]
  idx_pnt=[plm_tag.index(i) for i in pnt_prt]
  nplms=len(plms)
  nplgs=len(plgs)
  npnts=len(pnts)
#height for buildings must labelled in the name strings
  delim=',;_/ |-('
  hgts,nms=[],[]
  for ii in range(nplgs):
    i=idx_plg[ii]  
    ipas=0
    for d in delim:
      names[i]=names[i].strip(d)	
      if d in names[i]:
        if d=='(':names[i].replace(')')
        while d+d in names[i]:
          names[i].replace(d+d,d)
        hgts.append(float(names[i].split(d)[1].replace('m','').replace('M','')))
        nms.append(names[i].split(d)[0])
        ipas=1
        break
    if ipas==0:
      print ('name must contain building/stack height(m) for object:'+names[i])
      sys.exit('name must contain building/stack height(m) for object:'+names[i])


  #collect lon/lat for polygons
  lon=np.zeros(shape=(nplgs,5))
  lat=np.zeros(shape=(nplgs,5))
  for plg in plgs:
    iplg=plgs.index(plg)
    coord=plg.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
    c=coord[0].pyval.split()
    n=0
    P=[]	
    for ln in c:
      lon[iplg,n]=ln.split(',')[0]
      lat[iplg,n]=ln.split(',')[1]
      P.append(Point(lon[iplg,n],lat[iplg,n]))	  
      n+=1
    if len(c)<5:
      for i in range(len(c),5):
        lon[iplg,i]=lon[iplg,i-len(c)]
        lat[iplg,i]=lat[iplg,i-len(c)]
    if signed_area(Polygon(P[:]).exterior)<0: #correct to CCW
      ln=[lon[iplg,n-1-i] for i in range(len(c))]	
      lon[iplg,:]=ln[:]
      lt=[lat[iplg,n-1-i] for i in range(len(c))]	
      lat[iplg,:]=lt[:]
  #collect lon/lat for points

  lonp=np.zeros(shape=(npnts))
  latp=np.zeros(shape=(npnts))
  for pnt in pnts:
    ipnt=pnts.index(pnt)
    coord=pnt.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
    ln=coord[0].pyval.split()[0]
    lonp[ipnt]=ln.split(',')[0]
    latp[ipnt]=ln.split(',')[1]
  for k in range(npnts):
    ipas=0
    i=idx_pnt[k]
    for d in delim:
      names[i]=names[i].strip(d)
      if d in names[i]:
        while d+d in names[i]:
          names[i].replace(d+d,d)
        hgts.append(float(names[i].split(d)[1].replace('m','').replace('M','')))
        nms.append(names[i].split(d)[0])
        ipas=1
        break
    if ipas==0:nms.append(names[i])
  return nplgs,npnts,nms,hgts,lon,lat,lonp,latp

