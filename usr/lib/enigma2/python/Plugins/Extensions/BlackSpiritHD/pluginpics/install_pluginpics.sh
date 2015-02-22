#!/bin/bash
# This script is coded by DeadEyE for BlackSpirit.HD Skin (2/2015)
# You can change and use it for personal use only!



PICPATH="/usr/lib/enigma2/python/Plugins/Extensions/BlackSpiritHD/pluginpics"


if [ $1 = "installpics" ] ; then
		#make original
    if [ -f "$PICPATH/backup/pluginpicnewlist" ];then 
        for file in $(<$PICPATH/backup/pluginpicnewlist); do cp -a  $PICPATH/backup/$file "/usr/lib/enigma2/python/Plugins/$file"; done
    fi

    rm -f "$PICPATH/backup/pluginpiclist"
    
    #backup
    find $PICPATH/Extensions/* -type f | grep -o pluginpics/Extensions.*.png | grep -o Extensions.*.png  >> $PICPATH/backup/pluginpiclist
    for file in $(<$PICPATH/backup/pluginpiclist); do mkdir -p `dirname $PICPATH/backup/$file` && cp -a "/usr/lib/enigma2/python/Plugins/$file" $PICPATH/backup/$file; done

    cd $PICPATH/backup
		tar -f backup_pluginpics.tar -c *


    #install
    find $PICPATH/backup/Extensions/* -type f  | grep -o backup/Extensions.*.png | grep -o Extensions.*.png  > $PICPATH/backup/pluginpicnewlist
    for file in $(<$PICPATH/backup/pluginpicnewlist); do cp -a  $PICPATH/$file "/usr/lib/enigma2/python/Plugins/$file" ; done
fi

if [ $1 = "removepics" ] ; then
    for file in $(<$PICPATH/backup/pluginpicnewlist); do cp -a  $PICPATH/backup/$file "/usr/lib/enigma2/python/Plugins/$file"; done
    cd $PICPATH/backup
    rm -rf *
fi

exit 0
