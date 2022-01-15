kbdim ! max. block size

ztmp1(kdim)

ztmp1(1:kproma)     = fact_coll_eff*(ptp1tmp(1:kproma)-tmelt) !SF See #471
ztmp1(1:kproma)     = EXP(ztmp1(1:kproma))
zcolleffi(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma))

!UP comment: aggregation of ice crystals starts here
zc1(1:kproma) = 17.5_dp / crhoi * prho(1:kproma) * pqrho(1:kproma)**0.33_dp

ztmp1(1:kproma) = -6._dp / zc1(1:kproma) * LOG10(1.e4_dp*zris(1:kproma)) !SF zdt2
!SF Note: 1.e-4 = minimum size of snow flake
ztmp1(1:kproma) = ccsaut / ztmp1(1:kproma)

ztmp1(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma))

// ptp1tmp
    ptp1(kbdim)         ! temperature [celsius]
    plvdcp(kbdim)       ! latent heat of vaporization div. by specific heat at const pres.

    // pcnd
        // ztmp5
            pqp1(kbdim)         ! specific humidity [kg/kg]

            // zrhtest
                pqm1                ! specific humidity (t-1) [kg/kg]
                pqsm1               ! sat. specific humidity (t-1) over ice/water depending on temp [kg/kg]
                pqsp1tmp            ! temp new sat. specific humidity of ice/water depending on temp [kg/kg]
            zrhtest(kbdim)      ! temp variable needed for final calc. of condensation/deposition
        ztmp5(kbdim)        ! local temp variable with multiple meanings

        // ll5
            // lo2
                ptp1tmp(kbdim)      ! temporary variable of updated temp (t) [K] (redefined in line 4379, calculated in line 3676)
                pvervx(kbdim)       ! updraft velocity [cm/s]
            
                // zvervmax
                    pesw(kbdim)         ! saturation vapor pressure wrt water [Pa]
                    pesi(kbdim)         ! saturation vapor pressure wrt ice [Pa]
                    picnc(kbdim)        ! ice crystal number concentration (ICNC) [1/m3]
                    
                    // zrice
                        // ztmp1
                            picnc(kbdim)        ! ice crystal number concentration (ICNC) [1/m3]

                            // zxip1
                                pxip1(kbdim)        ! ice mass sedimentation (grid-mean values)
                                pxite(kbdim)        ! tendency of cloud ice from detrainment [kg/kg/s]
                                pxievap(kbdim)      ! evaporation of cloud ice [kg/kg]
                                pgenti(kbdim)       ! variable related to Tompkins cloud cover scheme

                                //pdep
                                    ztmp5
                                    ll5
                                pdep(kbdims)        ! deposition rate [kg/kg]
                            zxip1(kbdim)        ! cloud ice mass mixing ratio (t) [kg/kg]

                            prho(kbdim)         ! air density [kg/m3]
                            paclc(kbdim)        ! cloud cover
                        ztmp1
                    zrice(kbdim)        ! volume mean ice crystal radius needed for the Bergeron-Findeisen process
                    
                    peta(kbdims)        ! variable needed for the Bergeron-Findeisen process
                zvervmax(kbdim)     ! threshold vertical velocity needed for the Bergeron-Findeisen process        
            lo2(kbdim)          ! logical expression

            ll2(kbdim)              ! local temp variable with multiple meaning

            // ll3
                pqp1tmp(kbdim)      ! temp value of updated specific humidity (t) [kg/kg]
                zrhtest(kbdim)
            ll3(kbdim)          ! local temp variable with multiple meaning

            ll4(kbdim)          ! local temp variable with multiple meaning
        ll5(kbdim)          ! local temp variable with multiple meaning
    pcnd(kbdim)         ! condensation rate [kg/kg]

    plsdcp(kbdim)       ! latent heat of sublimation div. by the specific heat at const pres.
    pdep(kbdim)
ptp1tmp(kbdim)  


    
// zcolleffi
    ld_cc(kbdim)        ! logical expression
    pxib(kbdim)         ! cloud ice in cloudy part of grid box [kg/kg]
    ll1(kbdim)          ! logical expression
    ztemp1(kbdim)       ! local temp variable with multiple meanings 
zcolleffi(kbdim)        ! collision efficiency for aggregation (temp dependent)

// zc1
    prho(kbdim)         ! air density [kg/m3]
    pqrho(kbdim)        ! inverse air density [m3/kg]
zc1(kbdim)              ! temporary variable

// zris
    pxib(kbdim)         ! cloud ice in cloudy part of grid box [kg/kg]
    prho(kbdim)         ! air density [kg/m3]
    picnc(kbdim)        ! ice crystal number concentration (ICNC) [1/m3]
zris(kbdim)             ! size of ice crystals

ztemp1(kbdim)           ! local temp variable with multiple meanings 



ll3(1:kproma)       = (pqp1tmp(1:kproma)  < zrhtest(1:kproma))

pdep(1:kproma)      = MERGE(ztmp5(1:kproma), pdep(1:kproma), ll5(1:kproma))

zxip1(1:kproma)     = pxip1(1:kproma) + ztmst*pxite(1:kproma) - pxievap(1:kproma) + pgenti(1:kproma) + pdep(1:kproma)
zxip1(1:kproma)     = MAX(zxip1(1:kproma), 0._dp)
ztmp1(1:kproma)     = 1000._dp*zxip1(1:kproma)*prho(1:kproma)/MAX(paclc(1:kproma),clc_min)
ztmp1(:)            = eff_ice_crystal_radius(kbdim, kproma, ztmp1(:), picnc(:))
ztmp1(1:kproma)     = MIN(MAX(ztmp1(1:kproma), ceffmin), ceffmax)
zrice(:)            = effective_2_volmean_radius_param_Schuman_2011(kbdim, kproma, ztmp1(:))
zvervmax(:)         = threshold_vert_vel(kbdim, kproma, pesw(:), pesi(:), picnc(:), zrice(:), peta(:))  ==> Line3401
lo2(1:kproma)       = (ptp1tmp(1:kproma) < cthomi) .OR. (ptp1tmp(1:kproma) < tmelt .AND. 0.01_dp*pvervx(1:kproma) < zvervmax(1:kproma))

ll5(1:kproma)       = (.NOT. lo2(1:kproma)) .AND. ll2(1:kproma) .AND. ll3(1:kproma) .AND. ll4(1:kproma)

zrhtest(1:kproma)   = pqm1(1:kproma)/pqsm1(1:kproma)
zrhtest(1:kproma)   = MIN(zrhtest(1:kproma), 1._dp)
zrhtest(1:kproma)   = zrhtest(1:kproma)*pqsp1tmp(1:kproma)
ztmp5(1:kproma)     = pqp1(1:kproma)-zrhtest(1:kproma)
ztmp5(1:kproma)     = MAX(ztmp5(1:kproma), 0._dp)

pcnd(1:kproma)      = MERGE(ztmp5(1:kproma), pcnd(1:kproma), ll5(1:kproma))
ptp1tmp(1:kproma)   = ptp1(1:kproma) + plvdcp(1:kproma)*pcnd(1:kproma) + plsdcp(1:kproma)*pdep(1:kproma)


ll1(1:kproma)       = ld_cc(1:kproma) .AND. (pxib(1:kproma) > cqtmin)
zcolleffi(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma)) 

zc1(1:kproma)       = 17.5_dp / crhoi * prho(1:kproma) * pqrho(1:kproma)**0.33_dp

ztmp1(1:kproma)     = 1000._dp*pxib(1:kproma)*prho(1:kproma)
ztmp1(:)            = eff_ice_crystal_radius(kbdim, kproma, ztmp1(:), picnc(:))
ztmp1(1:kproma)     = MIN(MAX(ztmp1(1:kproma), ceffmin), ceffmax)
ztmp2(1:kproma)     = 5113188._dp+2809._dp*ztmp1(1:kproma)**3
ztmp2(1:kproma)     = SQRT(ztmp2(1:kproma))
ztmp2(1:kproma)     = -2261._dp + ztmp2(1:kproma)
ztmp3(1:kproma)     = 1.e-6_dp*ztmp2(1:kproma)**(1._dp/3._dp)
zris(1:kproma)      = MERGE(ztmp3(1:kproma), 1._dp, ll1(1:kproma))




REAL(dp) :: logarithm(kbdim), x(kbdim), ones(kbdim)

IF (lsimple_aggr) THEN
    ztmp1(1:kproma)     = fact_coll_eff*(ptp1tmp(1:kproma)-tmelt) !SF See #471
    ones(1:kproma)      = 1._dp
    ztmp1(1:kproma)     = ones(1:kproma) + ztmp1(1:kproma) !SK 1st order taylor series expansion for EXP(ztmp1(1:kproma))
    zcolleffi(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma))

    !UP comment: aggregation of ice crystals starts here
    zc1(1:kproma) = 17.5_dp / crhoi * prho(1:kproma) * pqrho(1:kproma)**0.33_dp

    !SK LOG10(1e4._dp*zris(1:kproma))
    !   = 4 + LOG10(zris(1:kproma))
    !   = 4 + LOG(zris(1:kproma))/LOG(10)
    !
    !   a = zris     b = 4     x = a * 10^b
    !   a = (1+x)/(1-x)     x = (a-1)/(a+1)
    !   LOG(a) = LOG((1+x)/(1-x)) = 2*(x + x^3/3 + x^5/5)

    x = (zris(1:kproma) - ones(1:kproma)) / (zris(1:kproma) + ones(1:kproma))

    logarithm(1:kproma) = 2._dp * (x + (x**3._dp)/3._dp + (x**5._dp)/5._dp) !SK 2nd order taylor series expansion for LOG((1+x)/(1-x))
    ones(1:kproma)      = 4._dp
    logarithm(1:kproma) = ones(1:kproma) + logarithm(1:kproma) / LOG(10._dp)
    ztmp1(1:kproma)     = -6._dp / zc1(1:kproma) * logarithm(1:kproma) !SF zdt2
    !SF Note: 1.e-4 = minimum size of snow flake
    ztmp1(1:kproma)     = ccsaut / ztmp1(1:kproma)

    ztmp1(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma))
ELSE
    ztmp1(1:kproma)     = fact_coll_eff*(ptp1tmp(1:kproma)-tmelt) !SF See #471
    ztmp1(1:kproma)     = EXP(ztmp1(1:kproma))
    zcolleffi(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma))

    !UP comment: aggregation of ice crystals starts here
    zc1(1:kproma) = 17.5_dp / crhoi * prho(1:kproma) * pqrho(1:kproma)**0.33_dp

    ztmp1(1:kproma) = -6._dp / zc1(1:kproma) * LOG10(1.e4_dp*zris(1:kproma)) !SF zdt2
    !SF Note: 1.e-4 = minimum size of snow flake
    ztmp1(1:kproma) = ccsaut / ztmp1(1:kproma)

    ztmp1(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma))
END IF
