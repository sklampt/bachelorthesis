#!/bin/bash 

########################
#
#Sylvaine Ferrachat 2013-06
#
# Script to compute the multi-annual means, timeseries, analysis over a given (equilibrium or not) period for a given
# set of cloud-microphysics-related quantities.
#
# The script produces 3 files:
#  * multi-annual_means_my_exp_YYYY1-YYYY2.nc --> geographical (2D or 3D) multi-annual means
#  * timeser_my_exp_YYYY1-YYYY2.nc            --> yearly time series of the global, multi-annual means
#  * analysis_my_exp_YYYY1-YYYY2.nc           --> global, multi-annual means
#
#########################

set -e

#-------------------------
# Define the below vars as env vars

#exp=rc2strat_ctrl                   # experiment name
#ext='.nc'                           # extension (leave empty for grib)
#root=/project/s235/sylvaine/${exp}  # root location of the data
#raw=${root}/Raw/                    # where to find the raw echam output
#dat=${root}/Data/                   # where to store the produced data
#wrk=${root}/Sandbox/                # where to execute the script, have temporary files etc...

#yb=2000    # year start
#ye=2049    # year end
#yb_eq=2025 # year to start computing equilibrium quantities if require (set it equal to yb if equilibirum is 
            # meaningless in your own context)

#codefile_date="201001.01"  # date to use for the txt code files for grib 

# end set custom vars
#-------------------------


#------------------------
# >UP: custom varviables to pass as arguments to the script call
# Now in prep_proc.sh (passing them like this does not make sense)
#smonth=${1:01}			     # starting month for your analysis (only makes sense if your analysis stays within the same year), default 01
#fmonth=${2:12}			     # finish month for your analysis (only makes sense if your analysis goes over less than one year), default 12
#flag_timemean=${3:true}	             # whether to compute the time mean
#<UP

# check: print out
echo "smonth="$smonth
echo "fmonth="$fmonth
echo "flag_timemean="$flag_timemean
# UP: end custom variables
#------------------------

#-- security:
exp=`sed -e 's|/||g' <<< "$exp"` # remove all '/' from $exp

#--- get cdo version (important for correct info parsing):
cdo_version=`cdo -V 2>&1 /dev/null | sed -n -e '1s/Climate Data Operators version \(.*\) (http.*$/\1/pg;'`

if [[ "$cdo_version" < "1.6" ]] ; then
   col_values=10
   col_vars=5
else
   col_values=9
   col_vars=11
fi

#--
cd ${wrk}


#-- test e6 vs e5
if [ -e ${raw}/${exp}_${yb}${smonth}.01_echam${ext} ] ; then
   flag_e6=true
   varname_tau="TAU_2D_550nm"
else
   flag_e6=false
   varname_tau="TAU_2D"
fi

echo "flag_e6="$flag_e6

#-- test presence _activ
if [ -e ${raw}/${exp}_${yb}${smonth}.01_activ${ext} ] ; then
   flag_activ=true
else
   flag_activ=false
fi

#-- test presence _rad
if [ -e ${raw}/${exp}_${yb}${smonth}.01_rad${ext} ] ; then
   flag_rad=true
else
   flag_rad=false
fi

#-- test presence _forcing
if [ -e ${raw}/${exp}_${yb}${smonth}.01_forcing${ext} ] && $flag_e6 ; then # the extracted forcing vars are only 
                                                                    # present in e6 output
   flag_forc=true
else
   flag_forc=false
fi

#-- test presence _burden (echam6-hammoz only)
if [ -e ${raw}/${exp}_${yb}${smonth}.01_burden.nc ] ; then # this '.nc' suffix has to be fixed in the output!!!
   flag_burd=true
else
   flag_burd=false
fi

#>UP
#-- test presence _echamm 
if [ -e ${raw}/${exp}_${yb}${smonth}.01_echamm.nc ] ; then # '.nc' suffix?
   flag_echamm=true
else
   flag_echamm=false
fi
#<UP

echo "flag_echamm="$flag_echamm

#-- Compute the total number of years
((nyears=$ye-$yb+1))

#-- Print summary:
echo "nyears="$nyears
echo "flag_activ="$flag_activ
echo "flag_rad="$flag_rad

#-- Initializations
\rm -f tmp*.nc

factnl=1.e-6
factni=1.e-3

#-- Prepare the cdo calculation file (with operator exprf):
cat > tmp_exprf.txt << EOF
SW=srad0;
SCRE=srad0-sraf0;
LW=trad0;
LCRE=trad0-traf0;
CFnet=srad0-sraf0+trad0-traf0;
Fnet=srad0+trad0;
SW_surf=srads;
LW_surf=trads;
LH=ahfl;
SH=ahfs;
Lf_snow=-aprs*333700.;
Fnet_surf=srads+trads+ahfl+ahfs-aprs*333700.;
Fnet_toa_min_surf=srad0+trad0-srads-trads-ahfl-ahfs+aprs*333700.;
CC=aclcov*100.;
LWP=xlvi*1.e3;
LWP_oc=xlvi_oc*1.e3;
IWP=xivi*1.e3;
PWAT=qvi;
Prcp_lsc=aprl*8.64e4;
Prcp_cv=aprc*8.64e4;
Prcp_tot=(aprl+aprc)*8.64e4;
Prcp_snow=aprs*8.64e4;
Prcp_rain=(aprl+aprc-aprs)*8.64e4;
Temp_srf=tsurf;
Temp_2m=temp2;
CC3d=aclcac*100;
LWC=xl*1.e6;
IWC=xi*1.e6;
TWC=(xl+xi)*1.e6;
Q=q*1.e3;
aps=aps;
geosp=geosp;
EOF

# What is accumulated?
#-----------------
# xlvi and xivi accumulated by default
# xl and xi only in echamm
# aclcov is

#-- Prepare a list of pressures for remapping over constant pressure levels

p0=100000
delta_p=2000
ndp=`echo "scale=0; $p0/$delta_p" | bc -l`
#echo $ndp
for ((i=0;i<$ndp;i++)) ; do
    p[$i]=`echo "scale=0; $p0-$i*$delta_p" | bc -l`
done

p_list=`echo ${p[@]}| tr " " ","`

#-- Loop over years and extract/compute proper vars:
for (( iy=$yb; iy<=ye; iy++ )) ; do

    echo $iy

    for ((im=${smonth}; im<=${fmonth}; im++)) ; do

        month=`printf '%02d' $im`
        rootname=${raw}/${exp}_${iy}${month}.01
        if $flag_e6 ; then
           file_echam=${rootname}_echam${ext}
           if [[ "$ext" == '' ]] ; then
              cdo_option_echam="-t ${raw}/${exp}_${codefile_date}_echam.codes"
           else
              cdo_option_echam=""
           fi
        else
           file_echam=${rootname}${ext}
           if [[ "$ext" == '' ]] ; then
              cdo_option_echam="-t ${raw}/${exp}_${codefile_date}.codes"
           else
              cdo_option_echam=""
           fi
        fi
           
        file_activ=${rootname}_activ${ext}
        if [[ "$ext" == '' ]] ; then
           cdo_option_activ="-t ${raw}/${exp}_${codefile_date}_activ.codes"
        else
           cdo_option_activ=""
        fi

        file_rad=${rootname}_rad${ext}
        if [[ "$ext" == '' ]] ; then
           cdo_option_rad="-t ${raw}/${exp}_${codefile_date}_rad.codes"
        else
           cdo_option_rad=""
        fi

        file_forc=${rootname}_forcing${ext}
        if [[ "$ext" == '' ]] ; then
           cdo_option_forcing="-t ${raw}/${exp}_${codefile_date}_forcing.codes"
        else
           cdo_option_forcing=""
        fi

        file_burd=${rootname}_burden.nc
	#>UP
        file_echamm=${rootname}_echamm.nc
	#<UP
  
        #--- part 1: usual analysis:

        cdo -O -s ${cdo_option_echam} -f nc selvar,srads,trads,ahfl,ahfs,srad0,sraf0,trad0,traf0,aclcov,slm,xlvi,xivi,aprl,aprc,aprs,tsurf,qvi,temp2,aclcac,xl,xi,q,aps,geosp $file_echam tmp_main.nc

        cdo -O -s ${cdo_option_echam} -f nc -chname,xlvi,xlvi_oc -ifnotthen -selvar,slm $file_echam \
                  -selvar,xlvi $file_echam tmp_lwp_oc.nc
        cdo -O -s merge tmp_lwp_oc.nc tmp_main.nc tmp_echam.nc
        
        cdo -O -s setctomiss,-9e+33 -exprf,tmp_exprf.txt tmp_echam.nc tmp1.nc
        
        cdo -O -s ${cdo_option_echam} -f nc sp2gp -chvar,st,Temp_tot -selvar,st ${file_echam} tmptemp.nc
        
        if $flag_activ ; then
           tmpactiv=tmpactiv.nc
	   # UP comment: below multiplication with 1.e-10 "means nothing but a convenient factor to avoid having a visually crowded vertical axis in the zonal mean plots" (SF)
           cdo -O -s ${cdo_option_activ} -f nc expr,'CDNC=CDNC_BURDEN*1.e-10;ICNC=ICNC_BURDEN*1.e-10;' \
                     -selvar,CDNC_BURDEN,ICNC_BURDEN $file_activ $tmpactiv
        else
           tmpactiv=""
        fi

        if $flag_rad ; then
           tmprad=tmprad.nc
           cdo -O -s ${cdo_option_rad} -f nc expr,"AOD=$varname_tau;" -selvar,$varname_tau $file_rad $tmprad
        else
           tmprad=""
        fi
    
        #--- part 2: get in-cloud CDNC, in-cloud icnc
        if $flag_activ ; then
            tmp_incl_cdnc=tmp_incl_cdnc.nc
            cdo -O -s ${cdo_option_activ} -f nc -setrtomiss,-inf,1.e-8 -selvar,CLOUD_TIME $file_activ \
                      tmp_cloud_liq_time.nc
            cdo -O -s ${cdo_option_activ} -f nc -selvar,CDNC_ACC $file_activ \
                      tmp_cdnc_acc.nc
            cdo -O -s chname,CDNC_ACC,incl_cdnc -mulc,$factnl -div tmp_cdnc_acc.nc tmp_cloud_liq_time.nc \
                      $tmp_incl_cdnc
    
            tmp_incl_icnc=tmp_incl_icnc.nc
            cdo -O -s ${cdo_option_activ} -f nc -setrtomiss,-inf,1.e-8 -selvar,CLIWC_TIME $file_activ \
                      tmp_cloud_ice_time.nc
            cdo -O -s ${cdo_option_activ} -f nc -selvar,ICNC_ACC $file_activ \
                      tmp_icnc_acc.nc
            cdo -O -s chname,ICNC_ACC,incl_icnc -mulc,$factni -div tmp_icnc_acc.nc tmp_cloud_ice_time.nc \
                      $tmp_incl_icnc

             tmp_wlarg_wconv=tmp_wlarg_wconv.nc
             cdo -O -s ${cdo_option_activ} -f nc -selvar,W_LARGE,W_TURB $file_activ \
                       $tmp_wlarg_wconv
        else
            tmp_inclcdnc=""
            tmp_incl_icnc=""
            tmp_wlarg_wconv=""
        fi

        #--- part 3: forcings
        if $flag_forc ; then
           tmp_forc=tmp_forc.nc
           cdo -O -s ${cdo_option_forcing} -f nc \
                -selvar,d_aflx_sw,d_aflx_swc,netht_sw,d_aflx_lw,d_aflx_lwc,netht_lw $file_forc $tmp_forc
        else
           tmp_forc=""
        fi

        #-- part 4: u,v,omega (vert velocity)
        cdo -O -s ${cdo_option_echam} -f nc selvar,u,v -dv2uv $file_echam tmp_u_v.nc

#        after $file_echam tmp.nc << EOF
#              &SELECT CODE=135, TYPE=20, MEAN=0, GRIB=1 &END  # GRIB?? <-- error?! should be FORMAT=1
#EOF
        after $file_echam tmp.nc << EOF
              &SELECT CODE=135, TYPE=20, MEAN=0, FORMAT=1 &END
EOF
        cdo -O -f nc chname,var135,omega tmp.nc tmp_omega.nc

        #-- part 5: aerosol burdens (echam-hammoz only)
        if $flag_burd ; then
           tmp_burd=tmp_burd.nc
           cdo -O -s selvar,burden_SO4,burden_BC,burden_OC,burden_DU,burden_SS $file_burd $tmp_burd
        else
           tmp_burd=""
        fi

	#>UP
        #-- part 6: LWC from echamm
        if $flag_echamm ; then
           tmp_echamm=tmp_echamm.nc
           cdo -O -s selvar,xi,xl $file_echamm $tmp_echamm
        else
           tmp_echamm=""
        fi
	#<UP

        #--- merge everything together:
	#UP: add tmp_echamm
        cdo -O -s merge tmp1.nc tmptemp.nc \
                        $tmprad \
                        $tmpactiv $tmp_incl_cdnc $tmp_incl_icnc $tmp_wlarg_wconv \
                        $tmp_forc \
                        tmp_u_v.nc tmp_omega.nc \
                        $tmp_burd \
			$tmp_echamm \
                        tmpfull_${iy}${month}.nc
    done 

    cdo -O copy tmpfull_${iy}??.nc tmp.nc 
    #>UP
    if $flag_timemean ; then
	    cdo -O timmean tmp.nc tmpfull_${iy}.nc
    else
	    cp tmp.nc ${dat}/tmp_${iy}.nc
    fi

    \rm -f tmpfull_${iy}??.nc tmp.nc
done

if ! $flag_timemean ; then
    echo "flag_timemean = false"
    #>UP
    #--- Annual means for process rates:
    # For now this works only without specifying the months
    # activ
    cdo -s -fldmean -vertsum ${raw}/${exp}_${yb}??.01_activ${ext} ${dat}/${exp}_${yb}${smonth}.01_activ${ext} 
    # echam
    cdo -s -fldmean -vertsum ${raw}/${exp}_${yb}??.01_echam${ext} ${dat}/${exp}_${yb}${smonth}.01_echam${ext} 
    #<UP
    exit
fi
#<UP

#--- Merge all years together:
cdo -O copy tmpfull_????.nc tmp.nc

#--- Prepare vertical averaging for time series and global average stats when relevant:
# (with special treatment to incl_cdnc and incl_icnc which comprise missing values --> creates
#  pbs with ml2pl)

if $flag_activ ; then
   nop=2
   op[0]="-delvar,aps,geosp -vertmean -ml2pl,$p_list -sp2gp -fldmean -delvar,incl_cdnc,incl_icnc" # for all vars
                                                                                  # but incl_cdnc and incl_icnc
   op[1]="-delvar,aps,geosp -vertmean -setctomiss,0. -ml2pl,$p_list -setmisstoc,0. "\
"-sp2gp -fldmean -selvar,aps,geosp,incl_cdnc,incl_icnc" #only for incl_cdnc and incl_icnc
else
   nop=1
   op[0]="-vertmean -ml2pl,$p_list -sp2gp -fldmean"
fi

#--- Timeseries: 

\rm -f tmp_ts_*.nc
for (( iop=0;iop<$nop;iop++ )) ; do
    eval cdo -O ${op[$iop]} tmp.nc tmp_ts_${iop}.nc
done
cdo -O merge tmp_ts_*.nc ${dat}/timeser_${exp}_${yb}-${ye}.nc

if [[ "$nyears" -gt 5 ]] ; then
   cdo -O runmean,5 ${dat}/timeser_${exp}_${yb}-${ye}.nc ${dat}/runavg_${exp}_${yb}-${ye}.nc
fi

#--- Multi-annual means:
cdo -O timmean -seldate,${yb_eq}-00-0000:00,${ye}-12-3123:59 tmp.nc \
       ${dat}/multi_annual_means_${exp}_${yb_eq}-${ye}.nc

#>UP
#--- Annual means for process rates:
# For now this works only without specifying the months
# activ
cdo -s ensmean ${raw}/${exp}_${yb}??.01_activ${ext} ${dat}/${exp}_${yb}.01_annual_activ${ext} 
cdo -s -fldmean -vertsum ${dat}/${exp}_${yb}.01_annual_activ${ext} ${dat}/${exp}_${yb}.01_annual_1d_activ${ext}
rm ${dat}/${exp}_${yb}.01_annual_activ${ext}
# echam
cdo -s ensmean ${raw}/${exp}_${yb}??.01_echam${ext} ${dat}/${exp}_${yb}.01_annual_echam${ext} 
cdo -s -fldmean -vertsum ${dat}/${exp}_${yb}.01_annual_echam${ext} ${dat}/${exp}_${yb}.01_annual_1d_echam${ext}
rm ${dat}/${exp}_${yb}.01_annual_echam${ext}
#<UP

#--- Final analysis text file:
cat > tmp.txt << EOF
${exp} averaged over ${yb_eq}-00-0000:00 to ${ye}-12-3123:59

Name                    Mean
EOF

\rm -f tmp_ga_*.nc
for (( iop=0;iop<$nop;iop++ )) ; do
    eval cdo -O ${op[$iop]} ${dat}/multi_annual_means_${exp}_${yb_eq}-${ye}.nc tmp_ga_${iop}.nc
done
cdo -O merge tmp_ga_*.nc tmp_ga_full.nc

cdo -O infov tmp_ga_full.nc |  \
    sed -e '1d' | \
    awk -v col_values=$col_values -v col_vars=$col_vars '{printf "%-20s%17.5g\n",$col_vars,$col_values}' >> tmp.txt

cat > comm.sed << EOF
/Name/a\\
-------------------------------------
/LCF/a\\
-------------------------------------
/Fnet/a\\
-------------------------------------
/PWAT/a\\
-------------------------------------
/Prcp_tot/a\\
-------------------------------------
/Temp_tot/a\\
-------------------------------------
/ICNC/a\\
-------------------------------------
/^\<CC3d\>/d
/^\<[LIT]WC\>/d
/^\<Q\>/d
/^\<Temp_tot\>/d
EOF

sed -f comm.sed tmp.txt > ${dat}/analysis_${exp}_${yb_eq}-${ye}.txt


#--- Cleanup:
\rm -f tmp*.nc comm.sed tmp*.txt

exit
