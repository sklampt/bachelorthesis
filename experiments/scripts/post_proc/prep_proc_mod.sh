#!/bin/bash

#------------------------------------------------------------------------------------------------------
# Sylvaine Ferrachat 2013-10
# Modified by Ulrike Proske 2021-02
#
# Script to prepare the usual p-proc on $PROJECT/$exp (launching of general_proc.sh)
# This produces the necessary subdirs, and create $PROJECT/$exp/Sandbox/wrap_general_proc.sh
# This script makes it easy to launch general_proc.sh via the batch system
#
# Usage:
# prep_proc.sh [-h] [-y YYYY-YYYY] [-q YYYY] [-e '.XX'] exp_name
#
# Options:
#  -h, --help
#         print this header
#
#  -y, --year-range [YYYY-YYYY]
#         set the year range, e.g. 2000-2009
#         default: 2000-2000
#
#  -q, --start-year-eq [YYYY]
#         set the starting year for multi-annual mean calculations (may be different from starting year when
#         running MLO exps for example, with taking only equilibirum values)
#         default: same as starting year
#
#  -e, --extension ['.XX']
#         set the file extension (.nc for netcdf, or '' for grib)
#         default: '.nc'
#
# Example:
# prep_proc.sh test
#
# The batch job is then launched with:
# cd $PROJECT/$exp/Sandbox/
# ./wrap_general_proc.sh
#
# Note:
# You may of course review and edit wrap_general_proc.sh before launching
#
#------------------------------------------------------------------------------------------------------

set -e

#-----------------------------------------------------
#-- Defaults initializations

flag_help=false
exit_code=0
queue_name="pproc"
y_range="2000-2000"
ext='.nc'
#>UP: custom variables
smonth=01 # starting month for your analysis (only makes sense if your analysis stays within the same year), default 01
fmonth=12 # finish month for your analysis (only makes sense if your analysis goes over less than one year), default 12 
flag_timemean=true # whether to compute the time mean
str_uname=`uname -n`
str_uname=${str_uname:0:2}
#<UP

#-----------------------------------------------------
#-- Handle options:

o_help="h"                        # print help
o_help_long="help"                # print help, long form
o_y_range="y"                     # year range
o_y_range_long="year-range"       # year range, long form
o_yb_eq="q"                       # starting year for equilibirum calculations
o_yb_eq_long="start-year-eq"      # starting year for equilibirum calculations, long form
o_ext="e"                         # extension
o_ext_long="extension"            # extension, long form
  

getopts_list="${o_help}${o_y_range}:${o_yb_eq}:${o_ext}:-:"

while getopts "$getopts_list" option ; do #loop over all options
    #-- translate the long options into short names first
    if [ "$option" == "-" ] ; then
        case $OPTARG in
             $o_help_long)
                option=$o_help
             ;;
             $o_y_range_long)
                option=$o_y_range
             ;;
             $o_yb_eq_long)
                option=$o_yb_eq
             ;;
             $o_ext_long)
                option=$o_ext
             ;;
             *)
             echo
             echo "Error! Unknown option!"
             echo
             flag_help=true
             exit_code=1
             ;;
        esac
    fi

    #-- Process all short (normal) options
    case $option in
         $o_help)
           flag_help=true
         ;;
         $o_y_range)
            if [ "$OPTARG" == "$o_y_range_long" ] ; then
               y_range="${!OPTIND}"
               ((OPTIND +=1))
            else
               y_range="$OPTARG"
            fi
         ;;
         $o_yb_eq)
            if [ "$OPTARG" == "$o_yb_eq_long" ] ; then
               yb_eq="${!OPTIND}"
               ((OPTIND +=1))
            else
               yb_eq="$OPTARG"
            fi
         ;;
         $o_ext)
            if [ "$OPTARG" == "$o_ext_long" ] ; then 
               ext="${!OPTIND}"
               ((OPTIND +=1))
            else
               ext="$OPTARG"
            fi
         ;;
    esac
done

#-----------------------------------------------------
#-- Normal arguments:

shift $((OPTIND-1)) # get rid of the options

if [[ "$#" -lt 1 ]] && ! $flag_help ; then
   echo "Error! You must provide at least 1 arguments!"
   echo
   flag_help=true
   exit_code=1
fi

if $flag_help ; then
   sed -n -e '3,/^#--------------------------/p' $0
   exit $exit_code
fi

exp=$1  # exp name

#-- Year-related vars
IFS='-' read -r yb ye <<< "$y_range"
if [ -z "$yb_eq" ]  ; then
   yb_eq=$yb
fi
y_code=$yb

#-- Subdir setup
rootdir=${PROJECT}/$exp
sdb=${rootdir}/Sandbox
dat=${rootdir}/Data

if [ ! -s $sdb ] ; then
   mkdir -p $sdb
fi

if [ ! -s $dat ] ; then
   mkdir -p $dat
fi

#-- Process
script="${sdb}/wrap_general_proc.sh"

if [ ${str_uname} = "ae" ] ; then
cat > $script << EOF
#!/bin/bash

exp="$exp"
root="${PROJECT}/\${exp}"

universal_wrap_batch.sh \\
	-q pproc \\
	${PROJECT}/scripts/general_proc_vari.sh \\
	02:00:00 \\
	exp="\$exp" \\
	ext="$ext" \\
	root="\$root" \\
	raw=\${root}/Raw \\
	dat=\${root}/Data \\
	wrk=\${root}/Sandbox \\
	yb=$yb \\
	ye=$ye  \\
	yb_eq=$yb_eq \\
	smonth=$smonth \\
	fmonth=$fmonth \\
	flag_timemean=$flag_timemean \\
	codefile_date="${y_code}01.01"
EOF
elif [ ${str_uname} = 'eu' ] ; then
cat > $script << EOF
#!/bin/bash

exp="$exp"
root="${PROJECT}/\${exp}"

universal_wrap_batch.sh \\
	${PROJECT}/echam_aerosol_scripts/general_proc_vari.sh \\
	00:30 \\
	exp="\$exp" \\
	ext="$ext" \\
	root="\$root" \\
	raw=\${root}/Raw \\
	dat=\${root}/Data \\
	wrk=\${root}/Sandbox \\
	yb=$yb \\
	ye=$ye  \\
	yb_eq=$yb_eq \\
	smonth=$smonth \\
	fmonth=$fmonth \\
	flag_timemean=$flag_timemean \\
	codefile_date="${y_code}01.01"
EOF
fi

chmod 755 $script

exit
