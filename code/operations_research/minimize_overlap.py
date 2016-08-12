import os
from gams import *

def get_overlap_model():
    return """
    Sets
        i trips ;

    Alias (i,ci) ;

    Parameters
        overlap(i,ci) overlap between trip i and trip ci ;

    Scalar n number of drivers ;

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load i overlap n
$gdxin

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

   Model trip /all/ ;
   Option mip = cplex ;
   Solve trip using mip minimizing z ;

   Display x.l, x.m, start.l, start.m, end.l, end.m ;
   """


def print_results_minimize_overlap(job):
    for rec in job.out_db["z"]:
        print "Minimal overlap(hours): %0.2f" % (rec.level/60.0/60)
    print "\n"

    for rec in job.out_db["x"]:
        if rec.level==1:
            print "x('%s', '%s'): level= %0.0f, marginal= %0.1f" \
                % (rec.key(0), rec.key(1), rec.level, rec.marginal)
    print "\n"

    for rec in job.out_db["start"]:
        if rec.level==1:
            print "start('%s'): level= %0.0f, marginal= %0.1f" \
                % (rec.key(0), rec.level, rec.marginal)
    print "\n"

    for rec in job.out_db["end"]:
        if rec.level==1:
            print "end('%s'): level= %0.0f, marginal= %0.1f" \
                % (rec.key(0), rec.level, rec.marginal)


def test():
    ws = GamsWorkspace(debug = DebugLevel.KeepFiles,
                       working_directory = os.getcwd())
    db = ws.add_database()

    trips = ['trip1', 'trip2', 'trip3', 'trip4', 'trip5']
    i = db.add_set("i", 1, "trips")
    for trip in trips:
        i.add_record(trip)

    overlap_data = { ('trip1', 'trip2'): 2,
                ('trip1', 'trip5'): 4,
                ('trip2', 'trip1'): 8,
                ('trip2', 'trip3'): 1,
                ('trip2', 'trip5'): 9,
                ('trip3', 'trip1'): 11,
                ('trip3', 'trip2'): 7,
                ('trip3', 'trip4'): 3,
                ('trip3', 'trip5'): 12,
                ('trip4', 'trip1'): 13,
                ('trip4', 'trip2'): 9,
                ('trip4', 'trip3'): 6,
                ('trip4', 'trip5'): 14,
                ('trip5', 'trip1'): 4,
               }
    overlap = GamsParameter(db, "overlap", 2, "overlap between trips")
    for k, v in overlap_data.iteritems():
        overlap.add_record(k).value = v

    n = GamsParameter(db, "n", 0, "number of drivers")
    n.add_record().value = 2

    job = GamsJob(ws, source=get_overlap_model())
    opt = GamsOptions(ws)

    opt.defines["gdxincname"] = db.name
    opt.all_model_types = "xpress"

    job.run(opt, databases = db)
    print_results_minimize_overlap(job)


if __name__ == "__main__":
    test()
