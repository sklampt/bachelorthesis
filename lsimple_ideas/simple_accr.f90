kbdim ! max. block size

ztmp1(kdim)

ztmp1(1:kproma) = cons4*zxsp(1:kproma)**0.8125_dp
ztmp1(1:kproma) = pi*cn0s*3.078_dp*ztmp1(1:kproma)*pqrho(1:kproma)**0.5_dp
ztmp1(1:kproma) = -ztmst*ztmp1(1:kproma)*zcolleffi(1:kproma)
ztmp1(1:kproma) = EXP(ztmp1(1:kproma))
ztmp1(1:kproma) = pxib(1:kproma) * (1._dp-ztmp1(1:kproma))



ld_cc(kbdim)        ! logical expression
pxib(kbdim)         ! cloud ice in cloudy part of grid box [kg/kg]
ll1(kbdim)          ! logical expression
pxsp1(kbdim)        ! ???
zxsp2(kbdim)        ! sno being formed inside grid box [kg/kg]
zxsp(kbdim)         ! snow mass mixing ratio [kg/kg]

pqrho(kbdim)        ! inverse air density [m3/kg]

zcolleffi(kbdim)    ! collision efficiency for aggregation (temp dependent)
                    ! comment UP: only used for accretion not aggregation




ll1(1:kproma)   = ld_cc(1:kproma) .AND. (pxib(1:kproma) > cqtmin)
zxsp2(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma)) ! snow that is formed inside grid box
zxsp(1:kproma)  = pxsp1(1:kproma) + zxsp2(1:kproma)

zcolleffi(1:kproma) = MERGE(ztmp1(1:kproma), 0._dp, ll1(1:kproma))




IF (lsimple_accr) THEN
    ztmp1(1:kproma) = cons4 * zxsp(1:kproma)**0.8125_dp
    ztmp1(1:kproma) = pi * cn0s * 3.078_dp * ztmp1(1:kproma) * pqrho(1:kproma)**0.5_dp
    ztmp1(1:kproma) = -ztmst * ztmp1(1:kproma) * zcolleffi(1:kproma)
   ! ztmp1(1:kproma) = cons4 * zxsp(1:kproma)**0.8125_dp * pi * cn0s * 3.078_dp * pqrho(1:kproma)**0.5_dp * (-ztmst) * zcolleffi(1:kproma) ! x
   ! ztmp1(1:kproma) = 1._dp + ztmp1(1:kproma) ! first order taylor series expansion e^x = 1 + x^1/1!
   ! ztmp1(1:kproma) = pxib(1:kproma) * (1._dp - ztmp1(1:kproma)) 
    ztmp1(1:kproma) = pxib(1:kproma) * (-ztmp1(1:kproma)) ! above two lines combined
ELSE
    ztmp1(1:kproma) = cons4*zxsp(1:kproma)**0.8125_dp
    ztmp1(1:kproma) = pi*cn0s*3.078_dp*ztmp1(1:kproma)*pqrho(1:kproma)**0.5_dp
    ztmp1(1:kproma) = -ztmst*ztmp1(1:kproma)*zcolleffi(1:kproma)
    ztmp1(1:kproma) = EXP(ztmp1(1:kproma))
    ztmp1(1:kproma) = pxib(1:kproma) * (1._dp-ztmp1(1:kproma))
END IF