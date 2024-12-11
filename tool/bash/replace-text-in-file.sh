#!bin/bash

echo -e "\nReplace Text in File\n"

OLD="#?#" # File to replace text
NEW="#?#" # New File output
DPATH="#?#" # Directory path
BPATH="/Users/air/Desktop/new-txt/" # Backup Folder
TFILE="/tmp/out.tmp.$$"
[ ! -d $BPATH ] && mkdir -p $BPATH || :
for f in $DPATH
do
  if [ -f $f -a -r $f ]; then
    /bin/cp -f $f $BPATH
   sed "s/$OLD/$NEW/g" "$f" > $TFILE && mv $TFILE "$f"
  else
   echo "Error: Cannot read $f"
  fi
done

cp -R /Users/air/Desktop/new-txt/ #output#

rm -rf "TFILE" /Users/air/Desktop/new-txt/
