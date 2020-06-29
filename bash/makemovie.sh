#########################################################
#	CREATE MOVIE FILE FROM IMAGE FILES  		#
#	Author: Srinivasa Babu Ramisetti		#
#  	Ecole Polytechnique Federale de Lausanne	#
#	Date:	09-September-2010			#
#	E-mail: ramisetti.srinivasa@epfl.ch		#
#	Web:	http://lsms.epfl.ch			#
#########################################################
# To do a movie ./makemovie.sh -d . -i png -o temp -f 10
#!/bin/sh

CommandExists()
{
    type -P "$1" &> /dev/null || { echo "WARNING: This script requires \"${1}\" but it's not installed. 
Please install it as follows: sudo apt-get install ${1} "; exit 1;}
}


usage()
{
cat << EOF
Usage: $0 options
This script is used to create movie from the image files.
OPTIONS:
   -h      Show usage
   -d	   Specify the directory path where the image files exists.
   -c      Specify video codec. Available codecs: mpeg4,msmpeg4,msmpeg4v2,wmv1,wmv2,rv10,mpeg1video,mpeg2video,mjpeg. Default: msmpeg4v2
   -i      Specify image format(Available format: jpeg,jpg,png). Default format: jpeg
   -f      Specify the frame per second. This is optional.
   -o	   Specify output file name. Default: movie
   -t	   Specify the desination directory to write the movie file. Default: Write at the same location as the image files location
   -v      Verbose
EOF
}

#################################################
#						#
#	Function supporting video codecs	#
#						#
#################################################
SetVideoFormat()
{
case $VCODEC in
  mpeg4)
    MOVFMT="avi"
    ;;
  msmpeg4)
    MOVFMT="mpeg"
    ;;
  msmpeg4v2)
    MOVFMT="mpeg"
    ;;
  wmv1)
    MOVFMT="wmv"
    ;;
  wmv2)
    MOVFMT="wmv"
    ;;
  rv10)
    MOVFMT="rv"
    ;;
  mpeg1video)
    MOVFMT="mpeg"
    ;;
  mpeg2video)
    MOVFMT="mpeg"
    ;;
  mjpeg)
    MOVFMT="avi"
    ;;    
    *)
    echo "Currenlty the program does not support $VCODEC codec format. EXITING!"
    exit 1
    ;;
esac
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
    ;;
  jpg)
    ;;
  png)
    ;;
    *)
    echo "Currenlty the program does not support $IMGFMT image format. EXITING!"
    exit 1
    ;;
esac
}

#################################################
#						#
#	Function to create movie files		#
#						#
#################################################
CreateMovie()
{
  TEMPFILE=$(mktemp Output.XXXXXXXXXX) || { echo "Failed to create temp file"; exit 1; }  
  FILTER=$(find $DIRECTORYPATH -type f \( -name "*.$IMGFMT" \) )
  ## nasty trick to check if image files of $IMGFMT exists ##
   if [[ -z ${FILTER} ]]
    then
      echo "No Image files of format $IMGFMT were found!. EXITING."
      exit
    else
      ls -1 $DIRECTORYPATH/*.$IMGFMT | sort -t "-" -n -k2,2 > $TEMPFILE
      if [ ${FPSFLAG} == "OFF" ]
      then
	  mencoder "mf://@$TEMPFILE" -o $DESTINATION/$OUTPUTNAME.$MOVFMT -ovc lavc -lavcopts vcodec=$VCODEC
      else
	  mencoder "mf://@$TEMPFILE" -mf fps=${FPS} -o $DESTINATION/$OUTPUTNAME.$MOVFMT -ovc lavc -lavcopts vcodec=$VCODEC
      fi
      #mencoder "mf://$DIRECTORYPATH/*.jpeg" -o movie.avi -ovc lavc -lavcopts vcodec=msmpeg4v2
      rm $TEMPFILE
    fi

}


#################################################
#						#
#	Main script begins from here		#
#						#
#################################################

###### Pre-requirement check for mencoder ######
#PreRequirements
CommandExists "mencoder";

###### Global variable decleration ######
DIRECTORYFLAG=0
DIRECTORYPATH=
DESTINATION=
IMGFMT=
OUTPUTNAME=
MOVFMT=
VCODEC="msmpeg4v2"
GImgHSIZE=1600
GImgVSIZE=1200
TITLE=
VERBOSE=
FPSFLAG="OFF"
FPS=

###### Script begins here ######
while getopts “hd:c:i:f:o:t:v” OPTION
do
  case $OPTION in
  h)
    usage
    exit 1
    ;;
  d)
    DIRECTORYFLAG=1
    DIRECTORYPATH=$OPTARG
    IMGFMT="jpeg"
    VCODEC="msmpeg4v2"
    MOVFMT="avi"
    OUTPUTNAME="movie"
    DESTINATION=$DIRECTORYPATH
    ;;
  c)
    VCODEC=$OPTARG
    ;;
  i)
    IMGFMT=$OPTARG
    ;;
  f)
    FPS=$OPTARG
    FPSFLAG="ON"
    ;;
  o)
    OUTPUTNAME=$OPTARG
    ;;
  t)
    DESTINATION=$OPTARG
    if [ -e $DESTINATION ]
    then
      DESTINATION=$OPTARG
    else
      echo "Target directory : $DESTINATION do no exist. EXITING!!!"
      exit
    fi
    ;;
  v)
    VERBOSE=1
    ;;
  ?)
  usage
    exit
    ;;
  *)
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

####### Check if the image format and video codec are supported ########
if [[ $DIRECTORYFLAG == 1 ]]
then
     SetImageFormat
     SetVideoFormat
fi

####### Actual process begins here ####### 
case $DIRECTORYFLAG in
  1)
    echo "Checking for image files in the directory..."
    if [ -d $DIRECTORYPATH ]
    then
      echo "Reading files..."
      CreateMovie
      echo "Done."
      exit
    else
      echo "Directory : $DIRECTORYPATH do no exist!."
    fi
    ;;
  0)
    echo "No directory provided.\n"
    echo "!!!EXITING!!!"
    exit 1
    ;;
esac
####### End of the script #########



######## Commented script for future reference ########
# sort files in correct order
#ls -1 yourdir | sort -t "-" -n -k2,2 -k3,3 -k4,4

#mencoder "mf://@temp.txt" -mf fps=25 -o output.avi -ovc lavc -lavcopts vcodec=mpeg4
#######################################################
