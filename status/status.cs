ST=/Library/WebServer/Documents/status.txt
date > $ST
for mdl in python mmif aermap aermod iscst cpuff;do
  n=$(ps -ef|grep $mdl|grep -v grep|wc -l)
  echo $n'\t'$mdl'\tjobs are running...' >> $ST
  if [ $n != 0 ]; then
    echo ' '>>$ST
    echo $(ps -ef|head -n1) >>$ST
    ps -ef|grep $mdl|grep -v grep >>$ST
    echo '\t'>>$ST
  fi
done
