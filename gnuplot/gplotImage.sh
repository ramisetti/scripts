#########################################################
#	CREATE IMAGE OF PLOT FROM XY DATA FILE  		#
#	Author: Srinivasa Babu Ramisetti		#
#  	Ecole Polytechnique Federale de Lausanne	#
#	Date:	08-September-2010			#
#	E-mail: ramisetti.srinivasa@epfl.ch		#
#	Web:	http://lsms.epfl.ch			#
#########################################################

#!/bin/sh
usage()
{
cat << EOF
Usage: $0 options
This script is used to create image of the plot drawn using the specified XY data file. The created image is written in the same location where the file exists.
OPTIONS:
   -h      Show usage
   -d	   Specify the directory path where the XY data files exists. NOTE: Use either -d or -f option.
   -f      XY Data filename. NOTE: Do not provide the file extension.
   -i      Specify image format(Available format: jpeg,png,eps,svg). Default format: jpeg
   -t	   Includes the user mentioned title for the plot. If not set, the file name is taken as the title.
   -v      Verbose
EOF
}

#################################################
#						#
#	Function to convert single XY 		#
#	       data file to image		#
#						#
#################################################

GPlotFunction()
{
FNAME=${FILENAME%\.*}
gnuplot << EOF
if($IMAGETYPE == 2) set terminal postscript eps color enhanced ;else set terminal $IMGFMT size $GImgHSIZE,$GImgVSIZE

set output "$FNAME.$IMGFMT"
set xlabel "Atom position"
set ylabel "Wave amplitude [A]"
set title "$TITLE"
set xrange [ $GRXMIN : $GRXMAX ]
set yrange [ $GRYMIN : $GRYMAX ]
plot "$FILENAME" using 1:2 notitle w l
EOF
}

#################################################
#						#
#	Function to convert XY data to		#
#	     images in a directory		#
#						#
#################################################

GPlotFunctionForFILESINFOLDER()
{
  SORTEDFILES=$(ls -1 $DIRECTORYPATH/*.plot | sort -t "-" -n -k2,2)
  #filestrings=$(echo $SORTEDFILES | tr "-" " ")

  for file in ${SORTEDFILES}
  do
    if [ -f $file ] ;
    then
      # name without extension
      name=${file%\.*}
      # get timestep field
      filename=${file%-*}
      len=${#filename}+1
      timestep='timestep'-${name:${len}}
      echo "Creating image $name.$IMGFMT"
gnuplot << EOF
  if($IMAGETYPE == 2) set terminal postscript eps color enhanced ;else set terminal $IMGFMT size $GImgHSIZE,$GImgVSIZE
  set xlabel "Atom position"
  set ylabel "Wave amplitude [A]"
  set output "$name.$IMGFMT"
  set title "$timestep"
  set xrange [ $GRXMIN : $GRXMAX ]
  set yrange [ $GRYMIN : $GRYMAX ]
  plot "$name.plot" using 1:2 notitle w l
EOF
    fi ;
  done
}

#################################################
#						#
#	Function supporting image formats	#
#						#
#################################################
SetImageFormat()
{
case $IMGFMT in
  jpeg)
    IMAGETYPE=0
    ;;
  jpg)
    IMAGETYPE=0
    IMGFMT="jpeg"
    ;;
  png)
    IMAGETYPE=1
    ;;
  eps)
    IMAGETYPE=2;
    ;;
  svg)
    IMAGETYPE=3;
    ;;
    *)
    echo "Currenlty the program does not support $IMGFMT image format. EXITING!"
    exit 1
    ;;
esac
}

#################################################
#						#
#	Main script begins from here		#
#						#
#################################################

###### Global variable decleration ######
FILEFLAG=0
FILENAME=
DIRECTORYPATH=
IMGFMT=
IMAGETYPE=0;
GImgHSIZE=1600
GImgVSIZE=1200
TITLE=
VERBOSE=
GRXMIN=-800
GRXMAX=800
GRYMIN=-0.0008
GRYMAX=0.0008

###### Script begins here ######
while getopts “hd:f:i:t:v” OPTION
do
  case $OPTION in
  h)
    usage
    exit 1
    ;;
  f)
    FILENAME=$OPTARG
    FILEFLAG=1
    IMGFMT="jpeg"
    TITLE=$FILENAME
    ;;
  d)
    DIRECTORYPATH=$OPTARG
    FILEFLAG=2
    IMGFMT="jpeg"
    ;;
  i)
    IMGFMT=$OPTARG
    ;;
  t)
    TITLE=$OPTARG
    ;;
  v)
    VERBOSE=1
    ;;
  ?)
  usage
    exit
    ;;
  esac
done

####### Show usage if run with no options ########
if [[ $# == 0 ]]
then
  usage
  exit
fi

####### Check if the image format is supported ########
if [[ $FILEFLAG == 1 ]] || [[ $FILEFLAG == 2 ]]
then
     SetImageFormat
fi

####### Actual process begins here ####### 
case $FILEFLAG in
  1)
    echo "Checking If File Exists..."
    if [ -f $FILENAME ]
    then
      GPlotFunction
      echo "Image creation done."
    else
      echo "File: $FILENAME do no exist!."
    fi
    ;;
  2)
    echo "Checking for files in the directory..."
    if [ -d $DIRECTORYPATH ]
    then
      echo "Reading files..."
      GPlotFunctionForFILESINFOLDER
      echo "Done."
    else
      echo "Directory : $DIRECTORYPATH do no exist!."
    fi
    ;;
  0)
    echo "No XYData files provided.\n"
    echo "!!!EXITING!!!"
    exit 1
    ;;
esac
####### End of the script #########