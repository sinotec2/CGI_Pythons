
#$1=pth
#$2=pid
LST=$1/CALPUFF.LST
OUT=$1/cpuff.out
touch $OUT
for ((i=0; i>=0;i+=1));do
  if [ -e $LST ];then 
    grep CONCENTRATIONS CALPUFF.LST |tail -n1 > $OUT
  else
    echo 'cpuff (pid='$2') has been executed for '${i}'0 seconds' >> $OUT
  fi
  now=$(ps -ef|grep cpuff721|grep $2 |grep -v grep|wc -l)  
  echo 'cpuff (pid='$2') has been executed for '${i}'0 seconds' >> $OUT
  all=$(ps -ef|grep cpuff721 |grep -v grep|wc -l)  
  echo 'All '${all}' cpuffs are executing' >> $OUT
  if [ $now != 1 ]; then break;fi
  sleep 10 
done
cd $1
cp ../demo/calpost.inp .
export PATH=/opt/anaconda3/envs/pyn_env/bin:$PATH
/Users/cpuff/src/CALPOST_v7.1.0_L141010/con2nc >& con2nc.out
ln -sf calpuff.con.S.grd02.nc cpuff.nc
/opt/local/bin/ncatted -a units,SO2,o,c,'ppbV'  -a units,NO2,o,c,'ppbV'  -a units,PM10,o,c,'ug/m3' -a units,SO4,o,c,'ug/m3' cpuff.nc
../demo/m3nc2gif.py cpuff.nc >& con2nc.out
cp -r /Library/WebServer/Documents/LC-GIF-Player/* .
mv *.gif example_gifs
cp ../demo/done.html prog.html
sed -ie 's/PID/'$2'/g' prog.html 
rand=$(echo $1|cut -d'_' -f3)
sed -ie 's/RAND/'$rand'/g'  prog.html
mb=$(ls -lh calpuff.con.S.grd02.nc|awk '{print $5}')
sed -ie 's/MB/'$mb'/g' prog.html

