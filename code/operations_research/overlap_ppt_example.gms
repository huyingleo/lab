    Sets
        i trips /trip1 * trip5/;

    Alias (i,ci) ;

    Table
        overlap(i,ci) overlap between trip i and trip ci
                trip1    trip2    trip3    trip4    trip5
        trip1    0        2        0        0        4
        trip2    8        0        1        0        9
        trip3    11       7        0        3        12
        trip4    13       9        6        0        14
        trip5    4        0        0        0        0    ;

    Scalar n number of drivers /2/;

    Variables
        x(i,ci)     from trip i to trip ci
        start(i)    start at trip i
        end(i)      end at trip i
        z           total overlap

    Binary Variable x, start, end ;

    Equations
        total_overlap    define objective function
        from_trip(i)
        to_trip(ci)
        start_trip
        end_trip
        self_trip(i) ;


   total_overlap..    z =e= sum((i,ci), x(i,ci)*overlap(i,ci)) ;
   from_trip(i)..     sum(ci, x(i,ci)) + end(i) =e= 1 ;
   to_trip(ci)..      sum(i, x(i,ci)) + start(ci) =e= 1 ;
   start_trip..       sum(i, start(i)) =e= n ;
   end_trip..         sum(i, end(i)) =e= n ;
   self_trip(i)..     x(i,i) =e= 0 ;

   Model trip /all/;
   Solve trip using mip minimizing z;

   Display x.l, x.m, start.l, start.m, end.l, end.m;
