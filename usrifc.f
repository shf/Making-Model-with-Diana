***  2006-10-10
*** FR≈N RIKARDS KALIBRERING AV SLƒTA LINOR
****subrutin usrifc, fungerar som beskrivet i avhandlingen och i rapport 99:5
****fungerar p‘ kawakami
****Programmerat fŒr ihopbakat rost+bondelement
****Rosten Ãr helt elastisk
***BŒrjat Ãndra fŒr att ta hÃnsyn till tjocka skikt - endast i both (ej i rost)
****Dessutom lÃgger till "litet avst‘nd" dÃr det kan rosta fritt
**** GŒr rosten icke-linjÃr Tn = K*erost^p 
**** StÃmmer med tidigare prorammering under p‘lastning ****
***  Har ordnat s‘ att rosten avlastas plastiskt med den styvhet som den hade om tn minskar. 
***  All rost som har belastats verkligen Ãr plastisk
***  R‰ttat fel i ATDM i subrutin FOUR, samt kriterie fˆr divergens i FOUR.

       SUBROUTINE USRIFC( U0, DU, NT, AGE0, DTIME, TEMP0, DTEMP,
     $          ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL, NUV,
     $          USRSTA, NUS, USRIND, NUI, TRA, STIFF )

       INTEGER   NUI, NT, NUV, USRIND(NUI), 
     $           ELEMEN, INTPT,  ITER, NUS
       CHARACTER*6  USRMOD
       DOUBLE PRECISION    U0(NT), DU(NT), AGE0, DTIME, TEMP0, DTEMP, 
     $          COORD(3), TRA(NT), STIFF(NT,NT), SE(NT,NT),  
     $          USRVAL(NUV), USRSTA(NUS),  US
 
       IF (USRMOD .NE. 'TWOD' .AND. USRMOD .NE. 'THREED' 
     $     .AND. USRMOD .NE. 'ROST' .AND. USRMOD .NE. 'BOTH' ) THEN   
           PRINT *, 'No model chosen in the inputfile'
           CALL PRGERR ('USRIFC', 1)
       ENDIF

       IF (USRMOD .EQ. 'TWOD' .AND. NT .NE. 2) THEN
              PRINT *, 'Wrong model chosen in the inputfile'
             CALL PRGERR ('USRIFC', 2)
       ENDIF

       IF (USRMOD .EQ. 'THRRED' .AND. NT .NE. 3) THEN
              PRINT *, 'Wrong model chosen in the inputfile'
             CALL PRGERR ('USRIFC', 3)
       ENDIF

      IF (USRMOD .EQ. 'TWOD' .OR. USRMOD .EQ. 'THREED') THEN
             CALL BOND( U0, DU, NT, AGE0, DTIME, TEMP0, DTEMP,
     $          ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL, NUV,
     $          USRSTA, NUS, USRIND, NUI, TRA, STIFF )
       ENDIF

      IF (USRMOD .EQ. 'BOTH' ) THEN
             CALL BOTH( U0, DU, NT, AGE0, DTIME, TEMP0, DTEMP,
     $          ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL, NUV,
     $          USRSTA, NUS, USRIND, NUI, TRA, STIFF )
       ENDIF


      IF (USRMOD .EQ. 'ROST') THEN
             USRSTA(1) = USRSTA(1)+DTIME
             US = (USRVAL(5)-USRVAL(3))
     $               /(USRVAL(4)-USRVAL(2))*USRSTA(1)
             STIFF(1,1)= USRVAL(1)/2/US
             TRA(1) = (U0(1)+DU(1)-US)*STIFF(1,1)
             STIFF(1,2)= 0
             STIFF(2,1)= 0  
             TRA(2) = STIFF(2,2)*(U0(2)+DU(2))
             IF (NT .EQ. 3 ) THEN
               STIFF(1,3) = 0
               STIFF(2,3) = 0
               STIFF(3,1) = 0  
               STIFF(3,2) = 0
               STIFF(3,3) = 3E11
               TRA(3) = TRA(3)+STIFF(3,3)*DU(3)
             ENDIF
       ENDIF

       END

************************************************************************
************************************************************************
       SUBROUTINE BOTH( U0, DU, NT, AGE0, DTIME, TEMP0, DTEMP,
     $          ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL, NUV,
     $          USRSTA, NUS, USRIND, NUI, TRA, STIFF )

       INTEGER   NUI, NT, NUV, USRIND(NUI), SOL, J, FLAG, TEU,
     $           ELEMEN, INTPT,  ITER, NUS, K, I, USRINDOLD(1)
       CHARACTER*6  USRMOD
       DOUBLE PRECISION    U0(NT), DU(NT), AGE0, DTIME, TEMP0, DTEMP, 
     $          COORD(3), TRA(NT), STIFF(NT,NT), SE(NT,NT),  
     $          USRVAL(NUV), USRSTA(NUS), KROST, V, EPROST,
     $          DX, X, HELP1, HELP2, DUB(2), TRAOLD(2), EPROSTMIN,  
     $          USRSTAOLD(7), TRANR, UBOND(2), A, R, F, P, MR, KR,  
     $          DUNBOLD, TRANBOLD, KB, MB, US, FDUNB , FDUNBOLD,
     $          FPRDUNB, DUBR1, DUBR, ALAST, DUBTN0, TRANITER,
     $          D12LASTSTEP, DUNB, DSSX, DSNZ, NR
   
       D12LASTSTEP = STIFF(1,2)   
       USRSTA(6) = USRSTA(6)+DTIME
       KROST = USRVAL(4+USRIND(2)*4+USRIND(3)*2+1)
       V = USRVAL(4+USRIND(2)*4+USRIND(3)*2+2)
       R = USRVAL(4+USRIND(2)*4+USRIND(3)*2+3)
       F = USRVAL(4+USRIND(2)*4+USRIND(3)*2+4)
       P = USRVAL(4+USRIND(2)*4+USRIND(3)*2+5)
******** calculate x and dx *********
****     avgˆr i vilket intervall man befinner sig i
       DO 10 I=0, (USRIND(3)-2)
         K = 5+USRIND(2)*4+I*2
         IF ( USRSTA(6) .GE. USRVAL(K) .AND.
     $       USRSTA(6) .LE. USRVAL(K+2) ) THEN
*            r‰tt intervall!
             DX = (USRVAL(K+3)-USRVAL(K+1))
     $               /(USRVAL(K+2)-USRVAL(K))
             X  = USRVAL(K+1) + DX*(USRSTA(6)-USRVAL(K))
         ENDIF
10     CONTINUE
       DX = DX * DTIME
       DUB(2) = DU(2)
       IF (NT .EQ. 3 ) THEN
        DUB(3) = DU(3)
        UBOND(3) = U0(3)
       ENDIF
********* Strain in the rust, in previous step ***************
       IF (X-DX .EQ. 0) THEN
         EPROST = 0
       ELSE
         A = -R + SQRT(R*R +(X-DX)*(V-1)*(2*R-X+DX))
         EPROST = (USRSTA(7)-A)/(X-DX+A)
       ENDIF
       EROST = P*KROST*EPROST**(P-1.0)
********* Rust layer *************
       A = -R + SQRT(R*R +X*(V-1)*(2*R-X))
******** Before the rust has filled the pores **********
       IF (A .LE. F) THEN
          SOL = 1
          DUB(1) = DU(1)
          USRSTA(7) = A
          UBOND(1) = U0(1)
          UBOND(2) = U0(2)
          CALL BOND( UBOND, DUB, NT, AGE0, DTIME, TEMP0, DTEMP,
     $          ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL, NUV,
     $          USRSTA, NUS, USRIND, NUI, TRA, STIFF )

       ELSE
******** When the rust starts to apply splitting stresses **********
******** First approximation of dunbond ************
          IF ( ABS(X-DX) .LT. 1E-10) THEN
*********** Special case when x is zero at the starting point, will fail with the other starting value  ***
            HELP1 = EROST+USRSTA(8)*X*V
            HELP2 = EROST*(DU(1)-DX*(V-1)) 
            DUB(1) = (HELP2 - STIFF(1,2)*DU(2)*V*X)
     $         / HELP1
          ELSE
            HELP1 = (X-DX)*(EROST+USRSTA(8)*(X-DX)*V)
            HELP2 = EROST*((X-DX)*DU(1)-DX*USRSTA(7)) 
            DUB(1) = (HELP2 - STIFF(1,2)*DU(2)*V*(X-DX)*(X-DX))
     $         / HELP1
          ENDIF
*            PRINT *, 'DUB(1)first', DUB(1)
************************************
          USRSTAOLD(1) = USRSTA(1)
          USRSTAOLD(2) = USRSTA(2)
          USRSTAOLD(3) = USRSTA(3)
          USRSTAOLD(4) = USRSTA(4)
          USRSTAOLD(5) = USRSTA(5)
          USRSTAOLD(7) = USRSTA(7)
          USRINDOLD(1) = USRIND(1)
          TRAOLD(1) = TRA(1)
          TRAOLD(2) = TRA(2)
          IF (NT .EQ. 3) THEN
            TRAOLD(3) = TRA(3)
          ENDIF
          I = 0        
          FLAG = 0
          TRANR = 1E20
          UBOND(1) = U0(1)-USRSTA(7) + F
          UBOND(2) = U0(2)
          DUBTN0 = 1E6
************ Starts by assuming that the rust is elastic, and solving the problem then ********* 
20        IF (ABS(TRANR-TRA(1)) .GT. 10 .OR. 
     $        ABS(DUNBOLD-DUB(1)) .GT. 1E-10 ) THEN
           IF(I .GE. 20) THEN
            SOL = 0
           ELSE
            SOL = 1
            I = I+1
            USRSTA(1) = USRSTAOLD(1)
            USRSTA(2) = USRSTAOLD(2)
            USRSTA(3) = USRSTAOLD(3)
            USRSTA(4) = USRSTAOLD(4)
            USRSTA(5) = USRSTAOLD(5)
            USRSTA(7) = USRSTAOLD(7)
            USRIND(1) = USRINDOLD(1)
            TRANBOLD = TRA(1)
            TRA(1) = TRAOLD(1)
            TRA(2) = TRAOLD(2)
            IF (NT .EQ. 3) THEN
              TRA(3) = TRAOLD(3)
            ENDIF
            CALL BOND( UBOND, DUB, NT, AGE0, DTIME, TEMP0, DTEMP,
     $          ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL, NUV,
     $          USRSTA, NUS, USRIND, NUI, TRA, STIFF )
            IF (TRA(1) .EQ. 0 .AND. FLAG .LE. 1
     $           .AND. USRSTA(8) .NE. 0 ) THEN
********** Solves for the smallest dunb which gives tn = 0, max twice ***********  
              IF ((-TRAOLD(1)-D12LASTSTEP*DU(2))/USRSTA(8)
     $            .LT. DUB(1)) THEN
                FLAG = FLAG+1
                DUB(1) = (-TRAOLD(1)-D12LASTSTEP*DU(2))/USRSTA(8)
*               PRINT *, 'DUB(1)justnoll', DUB(1)
              ENDIF
            ENDIF
            IF (TRA(1) .EQ. 0 .AND. FLAG .GT. 1) THEN
                IF (DUBTN0 .LT. DUB(1))THEN
                   DUB(1) = DUBTN0
                ELSE
                   DUBTN0 = DUB(1)
                ENDIF
            ENDIF
*            PRINT *, 'TRA(1)', TRA(1)
            IF (I .GE. 2 .AND. ABS(TRA(1)-TRANBOLD) .GT. 1
     $           .AND. ABS(DUB(1)-DUNBOLD) .GT. 1E-20 )THEN
********** Use of results from a previous iteration can be used, this speeds up the iteration ****
              KB = (TRA(1)-TRANBOLD)/(DUB(1)-DUNBOLD)
              MB = TRA(1) - KB*DUB(1)
              US =  U0(1) +DU(1) - UBOND(1) + F - A
              FDUNBOLD = 1E30
              FDUNB = 1E25
              DUNBOLD = DUB(1)
70            IF( ABS(FDUNB) .GE. 5 ) THEN
               IF( ABS(FDUNBOLD) .LE. ABS(FDUNB)) THEN
******************* divergence, uses then only one step ************
                 IF (ABS(FDUNB) .GT. 4) THEN
                   TRANR = TRA(1)
                   HELP1 = ABS(TRA(1)/KROST)
                   EPROST = -HELP1**(1.0/P)
                   USRSTA(7) = A+ (X+A)* EPROST 
                   DUNBOLD = DUB(1)
                   DUB(1) = U0(1) +DU(1) - USRSTA(7) + F - UBOND(1) 
                 ENDIF 
               ELSE 
******************* uses the results from the previous step ************
                 FDUNBOLD = FDUNB
                 FDUNB = KB*DUB(1)+MB - KROST*((US-DUB(1))/(X+A))**P
                 FPRDUNB= KB + P*KROST/(X+A)**P *(US-DUB(1))**(P-1.0)
                 DUB(1) = DUB(1) - FDUNB /  FPRDUNB
                 USRSTA(7) = U0(1) +DU(1) - UBOND(1) - DUB(1) + F
                 EPROST = (USRSTA(7)-A)/(X+A)
                 TRANR = KROST*EPROST**P       
                 GOTO 70
               ENDIF  
              ENDIF        
            ELSE
************* No earlier step that can be used *********
              TRANR = TRA(1)
              HELP1 = ABS(TRA(1)/KROST)
              EPROST = -HELP1**(1.0/P)
              USRSTA(7) = A+ (X+A)* EPROST 
              DUNBOLD = DUB(1)
              DUB(1) = U0(1) +DU(1) - USRSTA(7) + F - UBOND(1) 
            ENDIF
********************************************************************
*            PRINT *, 'DUB(1)', DUB(1)
            GOTO 20
           ENDIF
          ENDIF
********************************************************************

         IF ( TRA(1) .GT. USRSTA(9) .OR. SOL .EQ. 0 ) THEN
************* Unloading ********************************************
*********** Starts by checking if tn = 0 is a possible solution
           DUNBOLD = DUB(1)
           USRSTA(7) = A + USRSTA(10) 
           DUB(1) = U0(1) +DU(1) - USRSTA(7) + F - UBOND(1) 
*           PRINT *, 'DUB(1)unload - rust is zero', DUB(1)       
           USRSTA(1) = USRSTAOLD(1)
           USRSTA(2) = USRSTAOLD(2)
           USRSTA(3) = USRSTAOLD(3)
           USRSTA(4) = USRSTAOLD(4)
           USRSTA(5) = USRSTAOLD(5)
           USRSTA(7) = USRSTAOLD(7)
           USRIND(1) = USRINDOLD(1)
           TRA(1) = TRAOLD(1)
           TRA(2) = TRAOLD(2)
           IF (NT .EQ. 3) THEN
            TRA(3) = TRAOLD(3)
           ENDIF
          CALL BOND( UBOND, DUB, NT, AGE0, DTIME, TEMP0, DTEMP,
     $          ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL, NUV,
     $          USRSTA, NUS, USRIND, NUI, TRA, STIFF ) 
*           PRINT *, 'TRA(1)unload - zero?', TRA(1)  
           SOL = 1     
           IF (TRA(1) .NE. 0.0) THEN
************** Iteration krÃvs ***************************************'
             IF (USRSTA(12) .LT. 1E-30) THEN
************* Only the rust created in the step is elastic *********
                ALAST = -R + SQRT(R*R +(X-DX)*(V-1)*(2*R-(X-DX)))
             ELSE
************* There is earlier created rust that has never been loaded
                ALAST = -R + SQRT(R*R + USRSTA(12)*(V-1)*
     $             (2*R-USRSTA(12)))
                DX = X-USRSTA(12)
             ENDIF
             I = 0
             FLAG = 0 
******** First approximation of dunbond ************
             IF(TRAOLD(1) .LT. USRSTA(9)/2.0 ) THEN
               DUB(1) = DUNBOLD
             ELSE
               DUB(1) = 0
             ENDIF
*             PRINT *, 'DUB(1)firstunload', DUB(1)
             DUNBOLD = 1E6            
*************************************************************************
30           IF ( ABS(DUNBOLD-DUB(1)) .GT. 1E-8 
     $          .AND. ABS(TRANBOLD-TRA(1)) .GT. 10 ) THEN 
              IF(I .GE. 100) THEN
               SOL = 0
              ELSE
               SOL = 1
               I = I+1
               USRSTA(1) = USRSTAOLD(1)
               USRSTA(2) = USRSTAOLD(2)
               USRSTA(3) = USRSTAOLD(3)
               USRSTA(4) = USRSTAOLD(4)
               USRSTA(5) = USRSTAOLD(5)
               USRSTA(7) = USRSTAOLD(7)
               USRIND(1) = USRINDOLD(1)
               TRANBOLD = TRA(1)
               TRA(1) = TRAOLD(1)
               TRA(2) = TRAOLD(2)
               IF (NT .EQ. 3) THEN
                TRA(3) = TRAOLD(3)
               ENDIF
              CALL BOND( UBOND, DUB, NT, AGE0, DTIME, TEMP0, DTEMP,
     $             ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL,
     $             NUV, USRSTA, NUS, USRIND, NUI, TRA, STIFF )
               IF (TRA(1) .EQ. 0 .AND. FLAG .LE. 1
     $             .AND. TRANBOLD .NE. 0  .AND. USRSTA(8) .NE. 0 ) THEN
*************** Solves for the smallest dunb which gives tn = 0 , max three times ***********  
                 IF ((-TRAOLD(1)-D12LASTSTEP*DU(2))/USRSTA(8)
     $               .LT. DUB(1)) THEN
                   FLAG = FLAG + 1
                   DUB(1) = (-TRAOLD(1)-D12LASTSTEP*DU(2))/USRSTA(8)
*                  PRINT *, '********** Tn = 0 ********************'
*                  PRINT *, 'TRAOLD(2)', TRAOLD(2)
*                  PRINT *, 'DU(2)', DU(2)
*                  PRINT *, 'D12LASTSTEP', D12LASTSTEP
*                  PRINT *, 'USRSTA(8)', USRSTA(8)
*                  PRINT *, 'DUB(1)unloadjustnoll', DUB(1)
*                  PRINT *, 'TRAOLD(1)', TRAOLD(1)
                 ELSE
*************** TT is rather large, needs therefore a more thorough expression ***********
                  CALL GTC( '../MATERI/DSSX', DSSX, 1 )
                  CALL GTC( '../MATERI/DSNZ', DSNZ, 1 )
****testar att sÃtta d11 s‘ att den beror p‘ un***
                  IF ( U0(1)+DUB(1) .LE. 0 ) THEN
                      STIFF(1,1) = DSNZ
                  ELSE
                    IF ( U0(1)+DUB(1) .LE. 0.07E-3 ) THEN
                      STIFF(1,1) = DSNZ-(DSNZ-DSNZ/30)*
     $                   (U0(1)+DUB(1))/0.07E-3
                    ELSE        
                      STIFF(1,1) = DSNZ/1
                    ENDIF
                  ENDIF
                  IF ( U0(2)+DUB(2) .EQ. 0 ) THEN
                    IF (DUB(2) .EQ. 0) THEN
                      TEU = 1
                    ELSE 
                      TEU = ABS(DUB(2))/DUB(2)
                    ENDIF
                  ELSE
                    TEU = ABS(U0(2)+DUB(2))/(U0(2)+DUB(2))
                  ENDIF
                  DUNB = ((TRAOLD(2)+DSSX*DU(2) ) * 
     $               (STIFF(1,1)*USRVAL(3)+USRVAL(1))
     $              /(DSSX*TEU) -TRAOLD(1) - 
     $               TEU*USRVAL(1)*DU(2))  /STIFF(1,1)
*                  PRINT *, 'DUNB', DUNB

                  IF(DUNB .LT. DUB(1) ) THEN
                     FLAG = FLAG + 1
                     DUB(1) = DUNB
*                     PRINT *, '********** Tn = 0, spec. case! ********'
*                     PRINT *, 'DUB(1)unloadjustnoll', DUB(1)
                  ENDIF
                 ENDIF
               ENDIF
*               PRINT *, 'TRA(1)unload', TRA(1)

               IF (I .GE. 2 .AND. ABS(TRA(1)-TRANBOLD) .GT. 1E-5
     $              .AND. ABS(DUB(1)-DUNBOLD) .GT. 1E-20 ) THEN
********** Use of results from a previous iteration can be used, this speeds up the iteration ****
                 KB = (DUB(1)-DUNBOLD)/(TRA(1)-TRANBOLD)
                 MB = DUB(1) - KB*TRA(1)
                 US =  U0(1) +DU(1) - UBOND(1) + F - A
                 FDUNBOLD = 1E30
                 FDUNB = 1E25
                 FPRDUNB = 10
                 DUNBOLD = DUB(1)
                 IF (TRA(1) .EQ. 0.0 ) THEN
                   TRANITER = TRANBOLD/3
                 ELSE
                   TRANITER = TRA(1)
                 ENDIF
                 NR = 0.0
                 J = 0
80               IF(  ABS(FDUNB /  FPRDUNB) .GT. 10 ) THEN
                  IF( J .GT. 40) THEN
******************* divergence, uses then only one step ************
                    HELP1 = ABS(TRA(1)/KROST)
                    EPROST = -HELP1**(1.0/P)
                    USRSTA(7) = USRSTA(10)+A+ EPROST*(DX+A-ALAST)
     $                +USRSTA(11)*EPROST**P
                    DUB(1) = U0(1)+DU(1)-UBOND(1)+F-USRSTA(7)
                  ELSE 
****************** uses the results from the previous step ************
*               PRINT *, '***********************************' 
*               PRINT *, 'US',US 
*               PRINT *, 'USRSTA(10)', USRSTA(10)
*               PRINT *, 'MB', MB
*               PRINT *, 'TRANITER', TRANITER
*               PRINT *, 'USRSTA(11)', USRSTA(11)
*               PRINT *, 'KROST', KROST
*               PRINT *, 'KB',KB 
*               PRINT *, 'P', P
*               PRINT *, 'DX',DX 
*               PRINT *, 'A', A
*               PRINT *, 'ALAST', ALAST
                    J = J+1
                    FDUNBOLD = FDUNB
                    FDUNB = US -USRSTA(10)-MB
     $               -TRANITER*(USRSTA(11)/KROST+KB)
     $               +ABS(TRANITER)**(1.0/P)/KROST**(1.0/P)*(DX+A-ALAST)
                    FPRDUNB= -USRSTA(11)/KROST-KB - ABS(TRANITER)
     $                  **(1.0/P-1.0)/P/KROST**(1.0/P)*(DX+A-ALAST)
                    TRANITER = TRANITER - FDUNB /  FPRDUNB
                    DUB(1) = KB*TRANITER+MB
                    USRSTA(7) = U0(1) +DU(1) - UBOND(1) - DUB(1) + F
*               PRINT *, 'DUB(1)avlastiteration', DUB(1)
*               PRINT *, 'ABS(FDUNB /  FPRDUNB)', ABS(FDUNB /  FPRDUNB)
                    GOTO 80
                  ENDIF  
                 ENDIF
                 IF (TRANITER .GT. 0.0 .AND. NR .LE. 10) THEN
******************* Has found the wrong solution, tn must be less than zero ****
******************* Start the iteration once again, but from tn = 0 (numerically impossible, chose a value close to zero **
                    NR = NR+1.0
                    TRANITER = -1/NR
                    J = 0
                    FDUNB = 1E20
                    FPRDUNB = 1.0
                    GOTO 80
                 ENDIF 
*               PRINT *, 'TRANITER', TRANITER     
*               PRINT *, 'NR', NR   
               ELSE
************* No earlier step that can be used *********
                 HELP1 = ABS(TRA(1)/KROST)
                 EPROST = -HELP1**(1.0/P)
                 USRSTA(7) = USRSTA(10)+A+ EPROST*(DX+A-ALAST)
     $               +USRSTA(11)*EPROST**P
                 DUNBOLD = DUB(1)
                 DUB(1) = U0(1)+DU(1)-UBOND(1)+F-USRSTA(7)
               ENDIF
*               PRINT *, 'DUB(1)avlast', DUB(1)
               GOTO 30
              ENDIF
             ENDIF
************* Iteration ********
           ENDIF
*************Tn not equal to zero
************ H‘ller reda p‘ usrsta(10, 11 och 12) *******
           IF(ABS(USRSTA(12)) .LT. 1E-30  )THEN
             HELP1 = ABS(TRA(1)/KROST)
             EPROSTMIN = -HELP1**(1.0/P)          
             ALAST = -R + SQRT(R*R +(X-DX)*(V-1)*(2*R-(X-DX)))
             USRSTA(10) = USRSTA(10)+EPROSTMIN*(DX+A-ALAST)*(1-1/P) 
             IF (EPROSTMIN .NE. 0.0 )  THEN    
                USRSTA(11) = USRSTA(11)+(DX+A-ALAST)/
     $               (P*EPROSTMIN**(P-1))           
             ENDIF
           ENDIF
           IF(TRA(1) .EQ. 0.0 .AND. TRAOLD(1) .LT. 0.0 
     $            .AND. ABS(USRSTA(12)) .LT. 1E-30 )THEN
             USRSTA(12) = X
           ENDIF
         EROST = USRSTA(13)
         ENDIF         
***********Unloading
       ENDIF
********** filled the pores
********** total styvhet **************************
       USRSTA(8) = STIFF(1,1)
       IF (EROST .NE. 0.0) THEN 
         STIFF(1,1) = 1/ (1/USRSTA(8) + (X+A)/EROST)
       ENDIF   
*********** H‘ller reda p‘ max |tn| ***************
       IF ( TRA(1) .LT. USRSTA(9) ) THEN
           USRSTA(9) = TRA(1)
           USRSTA(13) = EROST
           HELP1 = ABS(USRSTA(9)/KROST)
           EPROSTMIN = -HELP1**(1.0/P)          
           USRSTA(10) = EPROSTMIN*(X+A)*(1-1/P)        
           USRSTA(11) = (X+A)/(P*EPROSTMIN**(P-1))        
       ENDIF

       IF (SOL .EQ. 0) THEN
            PRINT *, 'WARNING: Did not converge in both!!'
            PRINT *, 'Element', ELEMEN
            PRINT *, 'DUB(1)', DUB(1)
            PRINT *, 'DUNBOLD', DUNBOLD 
            PRINT *, 'TRA(1)min', USRSTA(9)
            PRINT *, 'TRA(1)bond', TRA(1)
            PRINT *, 'TRA(1)laststep', TRANBOLD
            IF((TRANITER .GT. TRA(1) .AND. TRANITER .LT. TRANBOLD) .OR.
     $       (TRANITER .LT. TRA(1) .AND. TRANITER .GT. TRANBOLD)) THEN
              TRA(1) = TRANITER
              PRINT *, 'Sets tn to', TRA(1)
            ENDIF
       ENDIF

       IF (ELEMEN .EQ. 40001 .AND. INTPT .EQ. 1) THEN
*        PRINT *, 'Element', ELEMEN
*        PRINT *, 'Erost', EROST
*        PRINT *, 'DU(1)', DU(1)
*        PRINT *, 'DU(2)', DU(2)
*        PRINT *, 'DUB(1)', DUB(1)
*        PRINT *, 'TRA(1)', TRA(1)
*        PRINT *, 'TRA(2)', TRA(2)
*        PRINT *, 'X', X
*        PRINT *, 'A', A
*        PRINT *, 'USRSTA(7)', USRSTA(7)
*        PRINT *, 'U0(1)', U0(1)
*        PRINT *, 'U0(2)', U0(2)
*        PRINT *, 'STIFF', STIFF
*        PRINT *, 'USRSTA', USRSTA
       ENDIF

       END

************************************************************************
************************************************************************
       SUBROUTINE BOND( U0, DUB, NT, AGE0, DTIME, TEMP0, DTEMP,
     $          ELEMEN, INTPT, COORD, SE, ITER, USRMOD, USRVAL, NUV,
     $          USRSTA, NUS, USRIND, NUI, TRA, STIFF )

       INTEGER   NUI, NT, NUV, USRIND(NUI), TE, SOL, TEU, 
     $           ELEMEN, INTPT,  ITER, NUS
       CHARACTER*6  USRMOD
       DOUBLE PRECISION   U0(NT), DUB(NT), AGE0, DTIME, TEMP0, DTEMP, 
     $          COORD(3), TRA(NT), STIFF(NT,NT), SE(NT,NT),  
     $          USRVAL(NUV), USRSTA(NUS), MY, DMY, C, DSNZ, DSSX,
     $          DC, F1, F2, ETA, B1, B2, B3, B4, TT, UTE,FA, DFA

       TT= TRA(2)
************ elastic **********
       CALL ELAST(STIFF,USRVAL,U0,DUB,TRA,NUV,TE,TEU,NT,ELEMEN)
*        PRINT *, 'TRA(1)el', TRA(1)
*        PRINT *, 'TRA(2)el', TRA(2)
************ uppdate c, my and eta **********
*****       n=U0(2)/5E-3
*****       IF( U0(2) .LT. 2.5e-3 ) THEN
*****                   ETA=USRVAL(3)
*****            ELSE
*****       IF  (U0(2)-n*5E-3 .GT. 2.5E-3 ) THEN
*****                   ETA=-0.3*USRVAL(3)
*****       ENDIF
*****       IF  (U0(2)-n*5E-3 .LT. 2.5E-3 ) THEN
*****                   ETA=0.3*USRVAL(3)
*****       ENDIF
*****       ENDIF
       ETA=USRVAL(3)
 
       CALL CMY(USRSTA(1),USRVAL,MY,DMY,C,DC,ETA,NUV,USRIND,
***  $   NUI,FA,DFA)
     $   NUI,FA,DFA)
*        PRINT *, 'KAPPA', USRSTA(1)
*        PRINT *, 'MY', MY
*        PRINT *, 'C', C
*         PRINT *, 'FA', FA
************ check damaged or undamaged deformation zone? **********
       CALL INTCCK ( TRA, USRSTA, USRIND, U0, DUB, TT,
     $            STIFF, NT, NUS, NUI,FA,DFA )
       IF ( USRIND(1) .NE. 0 ) THEN
            IF( U0(2) .GT. 0 ) THEN
                IF (USRSTA(5) .LT. 1E-6) THEN
                   UTE = 0
                ELSE
                   UTE = U0(2)/USRSTA(5)
                ENDIF
            ELSE
                IF (USRSTA(4) .GT. -1E-6) THEN
                   UTE = 0
                ELSE
                   UTE = U0(2)/USRSTA(4)
                ENDIF
            ENDIF
            IF ( U0(2)*DUB(2) . GT. 0 ) THEN
************** away from the original position ***********
               ETA = USRVAL(4)+ UTE*UTE*(ETA-USRVAL(4))
               MY = USRVAL(2)+ UTE*UTE*(MY-USRVAL(2))
            ELSE
************** towards the original position ***********
               ETA = USRVAL(4)
               MY = USRVAL(2)
            ENDIF
            DMY = 0
       ENDIF
***********************************************************
       F1 = ABS(TRA(2)) + MY*TRA(1)-MY*FA
       F2 = TRA(2)*TRA(2) + TRA(1)*TRA(1) + C*TRA(1)-FA*TRA(1)-FA*C 
***********************************************************
       IF (F1 .LE. 0  .AND. F2 .LE. 0) THEN
******* elastic ***********
*         PRINT *, '1'
           STIFF(1,2) = TEU* STIFF(1,2)
       ELSE
******** plastic *****************************************
         SOL = 0
******** calculate variables *********
         CALL BERVAR ( USRVAL, NUV, B1, B2, B3, B4, ETA, MY, C, 
     $      STIFF, TEU, TE, NT,FA)
         IF (F1 .GT. 0 .AND.  (TRA(1)-B3*TRA(2) + TE*B1*B3-B2 .GT. 0
     $      .OR. TRA(2) .EQ.0)) THEN
*********** region 2 eller 5********
            SOL= 1
            IF ( TRA(1)-B3*TRA(2) .GT. FA .OR. TRA(2) .EQ. 0) THEN
              CALL FIVE ( STIFF,TRA,USRSTA,MY,DMY,C,
     $                 DC,ETA, TE,USRIND,USRVAL,NUV,
****     $                 TEU, NT, NUI,NUS,FA,DFA)
     $                 TEU, NT,NUS,NUI,FA,DFA)
              STIFF(1,2) = TEU* STIFF(1,2)
            ELSE
              CALL TWO ( USRVAL, USRIND, STIFF, TRA, USRSTA, MY, 
     $           DMY, C, DC, ETA, TE, NUV, TEU,NT,NUI,NUS,FA,DFA)
              CALL TWOST ( STIFF, MY, TE, ETA, TEU, NT)
            ENDIF
         ENDIF

         IF ( SOL .EQ. 0 ) THEN
          IF ( F2 .GT. 0 .AND. (TRA(1)-B4*TRA(2)+TE*B1*B4-B2 
     $    .LT. 0 .OR. TRA(2).EQ.0)) THEN
*********** region 4 ********
            SOL= 1
            CALL FOUR ( STIFF, TRA, USRSTA, USRIND, USRVAL, NUV,
     $                 C, DC, TEU, NT, NUI, NUS,FA,DFA)
            IF (TRA(1)-B4*TRA(2)+TE*B1*B4-B2 .GT. 0 ) THEN
***           **passed the limit for region 3***
               TRA(1) = B2
               TRA(2) = TE*B1
*               PRINT *, 'passed the limit for 3 in element ', ELEMEN
*               PRINT *, 'MY', MY 
*               PRINT *, 'USRSTA', USRSTA 
            ENDIF
            CALL FOURST ( STIFF, TEU, TRA, C, NT,FA,DFA )
          ENDIF
         ENDIF

         IF ( SOL .EQ. 0 ) THEN
*********** region 3 ********
           CALL THREE ( STIFF, TRA, USRSTA, C, MY,
     $             TE, USRIND, USRVAL, NUV,TEU,NT,NUI,NUS,FA,DFA)
           CALL TWOST ( STIFF, MY, TE, ETA, TEU, NT )
         ENDIF

********** the limits of the undamaged deformations zone are adjusted, *********
********** only for plastic loading within undamaged deformation zone *********
     CALL GTC( '../MATERI/DSSX', DSSX, 1 )
     CALL GTC( '../MATERI/DSNZ', DSNZ, 1 )

         IF ( USRIND(1) .EQ. 0 ) THEN
           IF ( U0(2)+DUB(2)- TRA(2)/DSSX .GT. USRSTA(3) ) THEN
            USRSTA(3) =  U0(2)+DUB(2)- TRA(2)/DSSX
            USRSTA(5) =  U0(2)+DUB(2)
           ENDIF
           IF ( U0(2)+DUB(2) - TRA(2)/DSSX .LT. USRSTA(2) ) THEN
            USRSTA(2) = U0(2)+DUB(2)- TRA(2)/DSSX
            USRSTA(4) = U0(2)+DUB(2)
           ENDIF
         ENDIF

       ENDIF
*         PRINT *, 'TRA(1)', TRA(1)
*         PRINT *, 'TRA(2)', TRA(2)
       END

************************************************************************
************************************************************************
       SUBROUTINE ELAST(STIFF,USRVAL,U0,DUB,
     $     TRA,NUV,TE,TEU,NT,ELEMEN)
       INTEGER      NUV, TE, TEU, NT, ELEMEN
       DOUBLE PRECISION    STIFF(NT,NT), USRVAL(NUV), U0(NT),
     $       DUB(NT), TRA(NT), DSSX, DSNZ

      CALL GTC( '../MATERI/DSSX', DSSX, 1 )
      CALL GTC( '../MATERI/DSNZ', DSNZ, 1 )
**      STIFF(1,1)= DSNZ
      STIFF(2,2)= DSSX
****testar att sÃtta d11 s‘ att den beror p‘ un***
      IF ( U0(1)+DUB(1) .LE. 0 ) THEN
         STIFF(1,1) = DSNZ
      ELSE
         IF ( U0(1)+DUB(1) .LE. 0.07E-3 ) THEN
           STIFF(1,1) = DSNZ- (DSNZ-DSNZ/30)*
     $                   (U0(1)+DUB(1))/0.07E-3
         ELSE        
           STIFF(1,1) = DSNZ/30
         ENDIF
      ENDIF
*        PRINT *, 'STIFF(1,1)', STIFF(1,1) 
********************************************
        STIFF(2,1)= 0.0
        STIFF(1,2)= USRVAL(1)
        IF ( U0(2)+DUB(2) .EQ. 0 ) THEN
          IF (DUB(2) .EQ. 0) THEN
             TEU = 1
          ELSE 
             TEU = ABS(DUB(2))/DUB(2)
          ENDIF
        ELSE
          TEU = ABS(U0(2)+DUB(2))/(U0(2)+DUB(2))
        ENDIF
        TRA(1) = TRA(1)+STIFF(1,1)*DUB(1)+ TEU*STIFF(1,2)*DUB(2)
        TRA(2) = TRA(2)+STIFF(2,1)*DUB(1)+ STIFF(2,2)*DUB(2)
        IF (TRA(2) .EQ. 0.0) THEN
           TE = 1
        ELSE 
           TE = ABS(TRA(2))/TRA(2)
        ENDIF

        IF (NT .EQ. 3 ) THEN
          STIFF(1,3) = 0
          STIFF(2,3) = 0
          STIFF(3,1) = 0  
          STIFF(3,2) = 0
          STIFF(3,3) = 10E6
          TRA(3) = TRA(3)+STIFF(3,3)*DUB(3)
        ENDIF
       END
****************************************************************
       SUBROUTINE CMY(KAPPA,USRVAL,MY,DMY,
***     $             C,DC,ETA,NUV,USRIND,NUI,FA,DFA)
     $             C,DC,ETA,NUV,USRIND,NUI,FA,DFA)
       INTEGER     I ,  K, NUV, NUI, USRIND(NUI)
       DOUBLE PRECISION    USRVAL(NUV), KAPPA, MY, DMY, C, DC,
     $     ETA, FA,DFA
***         ETA = USRVAL(3)
******** calculate my and c *********
****     avgˆr i vilket intervall man befinner sig i
         DO 10 I=0, (USRIND(2)-2)
          K = 5+I*4
          IF ( KAPPA .GE. USRVAL(K) .AND.
     $       KAPPA .LE. USRVAL(K+4) ) THEN
****            r‰tt intervall!
             DC = (USRVAL(K+5)-USRVAL(K+1))
     $               /(USRVAL(K+4)-USRVAL(K))
             C  = USRVAL(K+1) + DC*(KAPPA-USRVAL(K))
             DMY = (USRVAL(K+6)-USRVAL(K+2))
     $                   /(USRVAL(K+4)-USRVAL(K))
             MY  = USRVAL(K+2) + DMY*(KAPPA-USRVAL(K))
             DFA = (USRVAL(K+7)-USRVAL(K+3))
     $                   /(USRVAL(K+4)-USRVAL(K))
             FA = USRVAL(K+3) + DFA*(KAPPA-USRVAL(K))
          ENDIF
10       CONTINUE
       END

****************************************************************
       SUBROUTINE BERVAR ( USRVAL, NUV, B1, B2, B3, B4,
     $      ETA, MY, C, STIFF, TEU, TE, NT,FA )
       INTEGER    NUV, TEU, TE, NT
       DOUBLE PRECISION    USRVAL(NUV), B1, B2, B3, B4,
     $    ETA, MY, C, FA, STIFF(NT,NT)

        B1 = MY*(C+FA)/(MY*MY+1)
        B2 = (MY*MY*FA-C)/(MY*MY+1)
        B3 = (STIFF(1,1)*ETA+STIFF(1,2))/(STIFF(2,2)*TEU)
        B4 = (STIFF(1,1)*(2*B2+C-FA) +TEU*STIFF(1,2)*2*B1) /
     $       (STIFF(2,2)*2*B1)
       END
****************************************************************
       SUBROUTINE FIVE ( STIFF,TRA,USRSTA,MY,DMY,C,
     $                 DC,ETA, TE,USRIND,USRVAL,NUV,
***     $                 TEU, NT, NUI, NUS,FA,DFA)
     $                 TEU, NT,NUI, NUS,FA,DFA)
***       INTEGER      USRIND(NUI), TEU, NT, NUS, NUI,TE, NUV
       INTEGER      NUI,USRIND(NUI), TEU, NT, NUS,TE, NUV
       DOUBLE PRECISION    STIFF(NT,NT),TRA(NT),USRSTA(NUS),
     $       TNE,TTE,FA,DFA, USRVAL(NUV),MY,DMY,C,F1,
     $                 DC,ETA

*         PRINT *, '5'
30       F1=TE*TRA(2)+MY*TRA(1)-MY*FA
         IF(ABS(F1) .GT. 1E-5)THEN        
         TNE = TRA(1)
         TTE = TRA(2)
         TRA(1)= FA
         TRA(2)= 0
           CALL CORNER ( STIFF, TRA, USRSTA, TNE, TTE, USRIND,
***     $                 TEU, NT, NUS, NUI,FA,DFA)
     $                 TEU, NT, NUS,NUI,FA,DFA)
         IF(USRIND(1) .EQ.0)THEN
           CALL CMY(USRSTA(1),USRVAL,MY,DMY,C,
***     $           DC,ETA,NUV,USRIND,NUI,FA,DFA)
     $           DC,ETA,NUV,USRIND,NUI,FA,DFA)
         END IF
         GOTO 30
       END IF
       END

****************************************************************
       SUBROUTINE CORNER (STIFF, TRA, USRSTA, TNE, TTE,
***     $      USRIND, TEU, NT, NUS, NUI,FA,DFA)
     $      USRIND, TEU, NT, NUS,NUI,FA,DFA)
***       INTEGER      USRIND(NUI), TEU, NT, NUS, NUI
       INTEGER      NUI,USRIND(NUI), TEU, NT, NUS
       DOUBLE PRECISION   STIFF(NT,NT), TRA(NT), USRSTA(NUS), 
     $                 TNE, TTE, DTN, DTT, UPN, UPT,FA,DFA

         DTN = TNE - TRA(1)
         DTT = TTE - TRA(2)
         UPN = DTN/STIFF(1,1) - TEU*STIFF(1,2)/
     $    (STIFF(1,1)*STIFF(2,2))*DTT
         UPT = DTT/STIFF(2,2)
         IF (USRIND(1) .EQ. 0) THEN
************** undamaged deformation zone ****************
           USRSTA(1) = USRSTA(1) + SQRT(UPN*UPN + UPT*UPT)
         ENDIF
       END

****************************************************************
       SUBROUTINE TWO ( USRVAL, USRIND, STIFF, TRA, USRSTA,
     $              MY, DMY, C, DC,ETA,TE,NUV,TEU,NT,NUI,NUS,FA,DFA)
       INTEGER     TE, NUI, USRIND(NUI), NUV, TEU, NT, NUS
       DOUBLE PRECISION   USRVAL(NUV), STIFF(NT,NT), TRA(NT), 
     $       USRSTA(NUS), MY, DMY, F1, ATDM, DLAMDA, 
     $       C, DC, ETA, F1OLD,FA,DFA
*         PRINT *, '2'
         F1OLD = 1E30
20       F1 = TE*TRA(2) + MY*TRA(1)-MY*FA
         IF (ABS(F1) .GE. ABS(F1OLD)) THEN
************** divergence *******
            PRINT *, 'WARNING: Does not converge on 
     $      material level in interface: 2'
*            PRINT *, 'USRVAL', USRVAL
*            PRINT *, 'USRIND', USRIND
*            PRINT *, 'USRSTA', USRSTA
*            PRINT *, 'MY', MY
*            PRINT *, 'DMY', DMY
*            PRINT *, 'TRA', TRA
*            PRINT *, 'F1', F1
*            PRINT *, 'TEU', TEU
*            PRINT *, 'ETA', ETA
*            PRINT *, 'STIFF', STIFF
            F1=0
         ENDIF
         IF (ABS(F1) .GT. 1E-5) THEN
             ATDM = STIFF(1,1)*MY*ETA + STIFF(1,2)*MY + 
     $              STIFF(2,2)*TEU*TE
             DLAMDA = F1/ (ATDM-DMY*TRA(1)*SQRT(ETA*ETA+1))
             IF (ABS(ATDM-DMY*TRA(1)*SQRT(ETA*ETA+1)) .LT. 1E-3) THEN
                PRINT *, 'Warning: almost division by zero'
             ENDIF
             TRA(1) = TRA(1) - DLAMDA*(ETA*STIFF(1,1)+STIFF(1,2))
             TRA(2) = TRA(2) - DLAMDA* TEU*STIFF(2,2)
             IF (USRIND(1) .EQ. 0) THEN
************** undamaged deformation zone ****************
                USRSTA(1) = USRSTA(1)+ DLAMDA*SQRT(ETA*ETA+1)
                CALL CMY (USRSTA(1),USRVAL,MY,DMY,C,DC
***     $          ,ETA,NUV,USRIND,NUI,FA,DFA)
     $          ,ETA,NUV,USRIND,NUI,FA,DFA)
             ENDIF
             F1OLD = F1
             GOTO 20
         ENDIF
       END

****************************************************************
       SUBROUTINE FOUR ( STIFF, TRA, USRSTA, USRIND, USRVAL, NUV,
     $                 C, DC, TEU, NT, NUI, NUS,FA,DFA)

       INTEGER      NUV, NUI, USRIND(NUI), TEU, NT, NUS
       DOUBLE PRECISION    STIFF(NT,NT), TRA(NT), USRSTA(NUS),
     $       USRVAL(NUV), C, DC,
     $              F2,MY,DMY,ATDM,DLAMDA,ETA,F2OLD,HE,HEL,FA,DFA

*         PRINT *, '4'
         F2OLD = 1E30
40       F2 = TRA(2)*TRA(2) + TRA(1)*TRA(1)
     $       + TRA(1)*C-FA*TRA(1)-FA*C
*            PRINT *, 'F2', F2
*            PRINT *, 'TRA', TRA
         IF (ABS(F2) .GE. ABS(F2OLD)*5) THEN
************** divergence
            PRINT *, 'WARNING: Did not converge on material
     $       level in interface: 4'
            PRINT *, 'F2', F2
            PRINT *, 'TRA', TRA
            F2=0
         ENDIF
         IF (ABS(F2) .GT. 10) THEN
            HE = 2*TRA(1)+C-FA
            HEL = DC*TRA(1)*SQRT(4*TRA(1)*TRA(1)+
     $            4*TRA(1)*C-4*TRA(1)*FA+C*C-FA*FA-FA*C+
     $            4*TRA(2)*TRA(2))
            ATDM = STIFF(1,1)*(4*TRA(1)*TRA(1)+4*TRA(1)*C-
     $             4*TRA(1)*FA+C*C-2*C*FA+FA*FA)+
     $             STIFF(1,2)*(4*TRA(2)*TEU*TRA(1)+
     $             2*TRA(2)*TEU*C-2*TRA(2)*TEU*FA)+
     $             STIFF(2,2)*4*TRA(2)*TRA(2)
            DLAMDA = F2/(ATDM-HEL)
*            PRINT *, 'HEL', HEL
*            PRINT *, 'ATDM', ATDM
*            PRINT *, 'C', C
*            PRINT *, 'DC', DC
*            PRINT *, 'DLAMDA', DLAMDA
    
           IF (ABS(ATDM-HEL) .LT. 1E-5) THEN
                PRINT *, 'Warning: almost division by zero'
           ENDIF
            TRA(1) = TRA(1) - DLAMDA*(STIFF(1,1)*HE
     $       + 2*TRA(2)*TEU*STIFF(1,2))
            TRA(2) = TRA(2) - DLAMDA* 2*STIFF(2,2)*TRA(2)
            IF (USRIND(1) .EQ. 0) THEN
************** undamaged deformation zone ****************
              USRSTA(1) = USRSTA(1)+DLAMDA*SQRT(4*TRA(1)*TRA(1)+
     $                    4*TRA(1)*C-4*TRA(1)*FA+C*C-FA*FA-FA*C+
     $                    4*TRA(2)*TRA(2))
              CALL CMY (USRSTA(1),USRVAL,MY,DMY,C,DC
***     $        ,ETA,NUV,USRIND,NUI,FA,DFA)
     $        ,ETA,NUV,USRIND,NUI,FA,DFA)
            ENDIF
            F2OLD = F2
            GOTO 40
         ENDIF
       END

****************************************************************
       SUBROUTINE THREE ( STIFF, TRA, USRSTA, C, MY,
     $                 TE, USRIND, USRVAL,NUV,TEU,NT,NUI,NUS,FA,DFA)
       INTEGER     TE, NUI, USRIND(NUI), NUV, TEU, NT, NUS
       DOUBLE PRECISION    STIFF(NT,NT), TRA(NT), USRSTA(NUS), C,
     $         DC, MY, DMY,TNE,TTE,USRVAL(NUV),ETA,F1,F2,FA,DFA

*         PRINT *, '3'
30       F1 = TE*TRA(2) + MY*TRA(1)-MY*FA
         F2 = TRA(2)*TRA(2) + TRA(1)*TRA(1) + TRA(1)*C-TRA(1)*FA-FA*C
*         PRINT *, 'F1', F1
*         PRINT *, 'F2', F2
         IF (ABS(F1) .GT. 1E-5 .OR. ABS(F2) .GT. 10) THEN
******    the tolerance of F2 is larger since in F2, the stresses are in square *****   
           TNE = TRA(1)
           TTE = TRA(2)
*         PRINT *, 'TNE', TNE
*         PRINT *, 'TTE', TTE
           TRA(1) = (MY*MY*FA-C)/(MY*MY+1)
           TRA(2) = TE*MY*(C+FA)/(MY*MY+1)
****           TRA(1) = (C-MY*MY*FA)/(MY*MY-1)
****           TRA(2) = TE*SQRT(FA*FA-2*MY*MY*FA*FA+2*C*FA*MY*MY-C*C)
****     $              *MY/(MY+1)*(MY-1)
*         PRINT *, 'TRA(1)', TRA(1)
*         PRINT *, 'TRA(2)', TRA(2)
           CALL CORNER ( STIFF, TRA, USRSTA, TNE, TTE,
***     $                  USRIND, TEU, NT, NUS, NUI,FA,DFA)
     $                  USRIND, TEU, NT, NUS,NUI,FA,DFA)
           IF (USRIND(1) .EQ. 0) THEN
************** undamaged deformation zone ****************
             CALL CMY (USRSTA(1),USRVAL,MY,DMY,C,
***     $                DC,ETA,NUV,USRIND,NUI,FA,DFA)
     $                DC,ETA,NUV,USRIND,NUI,FA,DFA)
           ENDIF
           GOTO 30
         ENDIF
       END

****************************************************************
       SUBROUTINE TWOST ( STIFF, MY, TE, ETA, TEU, NT)
       INTEGER     TE, TEU, NT
       DOUBLE PRECISION    STIFF(NT,NT), MY, ETA, HELP

         HELP= STIFF(1,1)*STIFF(2,2)/
     $         (STIFF(2,2)*TEU+STIFF(1,1)*ETA*MY*TE+TE*MY*STIFF(1,2))
         STIFF(1,1)= HELP*TEU
         STIFF(1,2)= -ETA*HELP
         STIFF(2,1)= -TE*TEU*MY*HELP
         STIFF(2,2)= MY*ETA*TE*HELP
       END

****************************************************************
       SUBROUTINE FOURST ( STIFF, TEU, TRA, C, NT,FA,DFA)
       INTEGER     TEU, NT
       DOUBLE PRECISION    STIFF(NT,NT), HELP, TRA(NT), C,FA,DFA

         IF (ABS(TRA(1)) .GT. 1E-5 .OR.  ABS(TRA(2)) .GT. 1E-5) THEN
           HELP = STIFF(1,1)*STIFF(2,2)/(-4*STIFF(2,2)*TRA(2)*TRA(2)+
     $     STIFF(1,1)*(4*TRA(1)*TRA(1)+4*TRA(1)*C-2*TRA(1)*FA+C*C-C*FA)-
     $     STIFF(1,2)*TRA(2)*TEU*(4*TRA(1)+2*C))
     $
           STIFF(1,1) = -4*TRA(2)*TRA(2)*HELP
           STIFF(1,2) = 2*TRA(2)*(2*TRA(1)+C-FA)*HELP
           STIFF(2,1) = (4*TRA(2)*TRA(1)+2*TRA(2)*C)*HELP
           STIFF(2,2) = (-4*TRA(1)*TRA(1)-4*TRA(1)*C+
     $                  2*TRA(1)*FA-C*C+C*FA)*HELP
         ENDIF
       END

****************************************************************
       SUBROUTINE INTCCK ( TRA, USRSTA, USRIND, U0, DUB, TT, 
     $                   STIFF, NT, NUS, NUI )
       INTEGER      NUI,USRIND(NUI), NT, NUS, U1
       DOUBLE PRECISION   TRA(NT), USRSTA(NUS), U0(NT), DUB(NT),
     $                   TT, STIFF(NT,NT)

        U1 = USRIND(1)
        
        IF ( USRIND(1) .EQ. 1 ) THEN
           IF (  U0(2)+DUB(2) - TT/STIFF(2,2) .LT. USRSTA(2)
     $           .OR. U0(2)+DUB(2) .LT. USRSTA(4) ) THEN
****  passing into undamaged deformation zone ****
               USRIND(1)=0
           ENDIF
        ENDIF

        IF ( USRIND(1) .EQ. -1 ) THEN
           IF (  U0(2)+DUB(2) - TT/STIFF(2,2) .GT. USRSTA(3)
     $           .OR. U0(2)+DUB(2) .GT. USRSTA(5)  ) THEN
****  passing into undamaged deformation zone ****
               USRIND(1)=0
           ENDIF
        ENDIF

        IF ( TRA(2) .LE. 0  .AND.  TT .GT. 0  
     $         .AND. DUB(2) .LT. 0 ) THEN
****  passing into damaged deformation zone ****
            USRIND(1) = 1
        ENDIF

        IF ( TRA(2) .GE. 0  .AND.  TT .LT. 0  
     $         .AND. DUB(2) .GT. 0 ) THEN
****  passing into damaged deformation zone ****
            USRIND(1) = -1
        ENDIF

        IF ( TRA(2) .LE. 0  .AND.  TT .GE. 0  
     $         .AND. DUB(2) .LT. 0 ) THEN
            IF ( U1 .EQ.-1) THEN
****  changing slip direction, still in damaged deformation zone ****
               USRIND(1) = 1
            ENDIF
        ENDIF

        IF ( TRA(2) .GE. 0  .AND.  TT .LE. 0  
     $         .AND. DUB(2) .GT. 0 ) THEN
            IF ( U1 .EQ. 1) THEN
****  changing slip direction, still in damaged deformation zone ****
               USRIND(1) = -1
            ENDIF
        ENDIF

        END

























