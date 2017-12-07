##### IMPORTANT NOTES ######
# This script is a wrapper to plot data using gnuplot
# This is in not a replacement to gnuplot but I use
# it particularly to save time to do repeating stuff
# By default the script will plot all columns in the datafile

if [ ${#@} -lt 1 ]; then
    echo "Usage: $0 datafile col (optional)"
    echo "e.g.: $0 data.dat"
    echo "e.g.: $0 data.dat 3"
    exit
fi

ifile="$1"
filename=$(basename "$ifile")
fext="${filename##*.}"
filename="${filename%.*}"

# switch flag_csv on to plot csv files 
flag_csv=0
# get max number of columns in the data file
mul_col=1
max_col=$(awk '!/^($|#|@)/{print NF; exit}' $ifile)
if [ $fext == "csv" ]; then 
    flag_csv=1;
    max_col=$(awk -F',' '!/^($|#|@)/{print NF; exit}' $ifile)
fi

if [ ${#@} -eq 2 ]; then
    col=$2
    if [[ ${2} -le $max_col ]] && [[ ${2} -ge 0 ]]; then    
	mul_col=0
	echo $col $mul_col
    else
	printf "Datafile has no %d column!\n" $col
	exit
    fi
fi

# invoke gnuplot to plot the data
gnuplot -p <<- EOF
#set print "-"
set ylabel "Energy (kJ.mol)"
set xlabel "Tip-surface separation (nm)"
set title "Free energy profile"
#set terminal pngcairo
#set output 'fep.png'

if ($flag_csv==1) set datafile separator ','

if ($mul_col==1) {
plot for [col=2:$max_col] '${ifile}' u 1:col w lp
}
if ($mul_col==0){
plot '$ifile' u 1:2 w lp notitle
}

EOF
