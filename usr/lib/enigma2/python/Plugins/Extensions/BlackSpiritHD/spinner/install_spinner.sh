#!/bin/bash
# This script is coded by DeadEyE for BlackSpirit.HD Skin (3/2015)
# You can change and use it for personal use only!


if [ $1 = "installspinner" ] ; then
    cp -a  /usr/lib/enigma2/python/Plugins/Extensions/BlackSpiritHD/spinner/img/* /usr/share/enigma2/BlackSpirit.HD/spinner/
fi

if [ $1 = "removespinner" ] ; then
    cd /usr/share/enigma2/BlackSpirit.HD/spinner
    rm -rf *
fi

exit 0
