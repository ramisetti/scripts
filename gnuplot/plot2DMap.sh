#!/usr/bin/bash

##### IMPORTANT NOTES ######
# This script plots 2D map of lammps data file
#
# author      : S.B.Ramisetti
# date        : 16/02/2018

# read input file
ifile=$1
# read timestep to plot the 2D map
step=$2

# count number of lines with comments
ncomments=$(awk '/^#/{count++} END{print count}' $ifile)
# read line number with 'Coord1' string
lineN=$(awk '/Coord1/{print NR}' $ifile)

# read column index for 'Coord1', 'Coord2', 'density/mass'
x_col_id=$(awk -v lN=$lineN '(NR==lN){ for (i=1; i<=NF; ++i) { if ($i ~ "Coord1$") print i-1 } }' $ifile)
y_col_id=$(awk -v lN=$lineN '(NR==lN){ for (i=1; i<=NF; ++i) { if ($i ~ "Coord2$") print i-1 } }' $ifile)
z_col_id=$(awk -v lN=$lineN '(NR==lN){ for (i=1; i<=NF; ++i) { if ($i ~ "density/mass$") print i-1 } }' $ifile)

# read time frequency 
timefreq=$(awk -v lN=$lineN '(NR==lN+1){ print $1 }' $ifile)
# read the number of rows for each timestep
nrows=$(awk -v lN=$lineN '(NR==lN+1){ print $2 }' $ifile)

#echo $x_col_id $y_col_id $z_col_id $nsteps $nrows

# extract start and end line numbers of data
line_sno=$(awk -v nc=$ncomments -v tf=$timefreq -v s=$step -v nr=$nrows 'BEGIN{print nr*((s/tf)-1)+nc+(s/tf)}')
line_eno=$(awk -v sno=$line_sno -v nr=$nrows 'BEGIN{print nr+sno}')
#echo $line_sno $line_eno

# extract data between start and end line numbers and copy to tmp0 file
awk -v sno=$line_sno -v eno=$line_eno 'NR>sno && NR <=eno' $ifile > tmp0

# process tmp0 to insert blank lines so splot can plot the 2D map
awk -v col=$x_col_id '
$col != prev {printf "\n"; prev=$col} # print blank line  
{print} # print the line
' tmp0 > tmp

# invoke gnuplot to plot the data
gnuplot -p <<- EOF
set print "-"
set cntrparam levels 10
set samples 25, 25
set isosamples 50, 50
set palette rgbformulae 34,35,0;
set view map; 
#set dgrid3d 124,112 splines
set pm3d interpolate 10,10; 
splot "tmp" u $x_col_id:$y_col_id:$z_col_id w pm3d notitle

EOF

rm tmp0 tmp
