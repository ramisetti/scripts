#############################################################
#	Convert OpenFAST output file to tab-delimited file  #
#	Authors: Srinivasa B. Ramisetti     	    	    #
#	Created:   26-June-2020		  	            #
#	E-mail: ramisettisrinivas@yahoo.com		    #
#	Web:	http://ramisetti.github.io		    #
#############################################################
#!/usr/bin/env bash

if [ ${#@} -lt 1 ]; then
    echo "Usage: $0 datafile"
    echo "e.g.: $0 data.dat"
    echo "On successful completion, the tab-delimited output file 'data-tab.dat' is created"
    exit
fi

iname=$1
head -6 $iname > ttemp1
#awk 'NR==9||NR==10{sub(/^ */, "")}' $iname > ttemp2

awk 'NR>8 {$1=$1;print}' $iname > ttemp02
tr ' ' '\t' < ttemp02 > ttemp12
sed 's/WaveElev/Wave1Elev/g' ttemp12 > ttemp2
ofile="${iname%.*}-tab.txt"

#echo $ofile
cat ttemp1 ttemp2 > $ofile

# remove temporary files
rm ttemp1 ttemp02 ttemp12 ttemp2
