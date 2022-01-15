#!/bin/bash

#------------------------------------------------------------------------------------------------------
# Sylvaine Ferrachat 2015-01
#
# Script to create hard links of raw output of echam to a 'project' directory 
#
# This script needs the following environment variables to be defined prior to running it:
#
#  - exp             # experiment name
#  - exp_dir         # where the echam output is
#  - p_proc_dir      # where the echam output is to be hardlinked. This will be created if necessary
#
#------------------------------------------------------------------------------------------------------

exp=""
exp_dir="${PROJECT}/../work/${exp}/"
p_proc_dir="${PROJECT}/${exp}/Raw"

set -e

#-----------------------------------------------------------------------
#-- Start

    cd $exp_dir

#-----------------------------------------------------------------------
#-- Create the p-proc directory if necessary (and parents)

    if [ ! -s $p_proc_dir ] ; then
       mkdir -p $p_proc_dir
    fi

#-----------------------------------------------------------------------
#-- Synchronizes all echam output to the p-proc directory

    echo "Creating hardlinks for:"
    echo "${exp}_* and r*_${exp}_*"
    echo "found in:"
    echo "$exp_dir"
    echo "into:"
    echo "$p_proc_dir"

    for file in `find $exp_dir -name "${exp}_*" -or -name "r*_${exp}_*"` ; do
        ln -f $file $p_proc_dir
    done

exit
