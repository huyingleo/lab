    Sets
        i              deliveries / d1 * d5 / ;

    Alias (i, ci) ;

    Parameters
        actime(i)    accumulated time spend on driving and picking up
                       / d1     4059
                         d2     4986
                         d3     5912
                         d4    11037
                         d5    11099 /

        due(i)         due timestamp
                       / d1    1394755200
                         d2    1394756086
                         d3    1394757063
                         d4    1394762400
                         d5    1394762400 /


    Scalar start       timestamp of start time
                       / 1394748000 / ;

    variables
        x(i)           idle time
        z              total time error ;

    Positive Variable x;
    x.UP(i) = 4*60*60 ;
    
    Equations
        time_error     define objective function ;

    time_error..       z =e= sum(i, abs(start+actime(i)+sum(ci$[ord(ci)<=ord(i)],x(ci))-due(i))) ;

    Model driver /all/ ;

    Solve driver using dnlp minimizing z ;

    Display x.l, x.m ;
