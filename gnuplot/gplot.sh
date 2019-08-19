##### IMPORTANT NOTES ######
# This script is a wrapper to plot data using gnuplot
# This is in not a replacement to gnuplot but I use
# it particularly to save time to do repeating stuff
# by default the script will plot all columns in the datafile
# The script does not work in the case of spaces in optional
# variables.
#
# author      : S.B.Ramisetti
# date        : 09/12/2017

if [ ${#@} -lt 1 ]; then
    echo "Usage: $0 datafile -col -xrange -yrange -xlabel -ylabel -title -png"
    echo "e.g.: $0 data.dat"
    echo "e.g.: $0 data1.dat data2.dat"
    echo "e.g.: $0 data1.dat data2.dat -col=4"
    echo "e.g.: $0 data1.dat data2.dat -col=6 -xrange=2:10"
    echo "e.g.: $0 data1.dat data2.dat -col=8 -xlabel=displacement_in_nm"
    echo "e.g.: $0 data1.dat data2.dat -col=1 -title=force_vs_displacement"
    echo "e.g.: $0 data1.dat data2.dat -col=2 -png=output.png"
    exit
fi

col=-1
mul_col=1; 
flag_png=0; flag_xlab=0; flag_ylab=0; flag_title=0;
for var in "$@"
do
    case $var in
	-col=*)
	col="${var#*=}"
	mul_col=0
	shift
	;;
	-xrange=*)
	tmp="${var#*=}"
	tmp="xrange[$tmp]"
	settings=("${settings[@]}" $tmp)
	shift
	;;
	-yrange=*)
	tmp="${var#*=}"
	tmp="yrange[$tmp]"
	settings=("${settings[@]}" $tmp)
	shift
	;;
	# deal settings with spaces separately
	-xlabel=*)
	flag_xlab=1
	xlabel="${var#*=}"
	shift
	;;
	-ylabel=*)
	flag_ylab=1
	ylabel="${var#*=}"
	shift
	;;
	-title=*)
	flag_title=1
	title="${var#*=}"
	shift
	;;
	-png=*)
	flag_png=1
	pngfile="${var#*=}"
	shift
	;;
	*)
	file_list=("${file_list[@]}" $var)
	;;
    esac
done

echo "Plotting files :" 
for file in ${file_list[@]}
do 
    filename=$(basename "$file")
    fext="${filename##*.}"
    filename="${filename%.*}"
    printf "%s \n" $file

    # switch flag_csv on to plot csv files 
    flag_csv=0
    # get max number of columns in each data file
    maxnum=$(awk '!/^($|#|@)/{print NF; exit}' $file)
    if [ $fext == "csv" ]; then 
	flag_csv=1;
	maxnum=$(awk -F',' '!/^($|#|@)/{print NF; exit}' $file)
    fi
    max_col=("${max_col[@]}" $maxnum)

    if [ $mul_col == 0 ]; then
	if [[ $col -gt $maxnum ]] || [[ $col -lt 0 ]]; then
            printf "Datafile %s has no column: %d !\n" $file $col
            exit
	fi
    fi
done


# invoke gnuplot to plot the data
gnuplot -p <<- EOF
#set terminal vttek
set print "-"

settings="${settings[*]}"
files="${file_list[*]}"
cols="${max_col[*]}"

if ($flag_png==1) { set terminal pngcairo;  set output '$pngfile' }
if ($flag_csv==1) set datafile separator ','
do for [val in settings] {
    eval('set '.val)
}
if ($flag_xlab==1) set xlabel '$xlabel'
if ($flag_ylab==1) set ylabel '$ylabel'
if ($flag_title==1) set title '$title'

do for [val in files] {
max_col(val)=system((sprintf("awk '!/^($|#|@)/{print NF; exit}' %s",val)))
#print " : ",max_col(val), val
}

if ($mul_col==1) {
    plot for [file in files] for [icol=2:max_col(file)] file u 1:icol w lp title file
}
if ($mul_col==0){
    plot for [file in files] file u 1:$col w lp notitle
}

EOF
