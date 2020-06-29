#!/bin/bash

unsetenv DISPLAY

nohup ~/matlabR2009a/bin/matlab -nodisplay -r "run $1" >$2 2>&1 &