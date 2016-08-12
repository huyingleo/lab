import os
from gams import *

def get_time_error_model():
    return """
    Sets
        i              deliveries ;

    Alias (i, ci) ;

    Parameters
        actime(i)      accumulated time spend on driving and picking up
        due(i)         due timestamp ;

    Scalar start       timestamp of start time ;

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load i actime due start
$gdxin

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
    """


def print_results_minimize_time_error(job):
    for rec in job.out_db["z"]:
        print "Minimal time errors (minutes): %0.2f" % (rec.level/60.0)
    print "\n"

    for rec in job.out_db["x"]:
        print "x('%s'): level= %0.0f, marginal= %0.1f" \
            % (rec.key(0), rec.level, rec.marginal)


def test():
    ws = GamsWorkspace(debug = DebugLevel.KeepFiles,
                       working_directory = os.getcwd())
    db = ws.add_database()

    deliveries = ['delivery1', 'delivery2', 'delivery3', 'delivery4', 'delivery5']
    i = db.add_set("i", 1, "deliveries")
    for delivery in deliveries:
        i.add_record(delivery)

    actime_data = { "delivery1": 4059,
                    "delivery2": 4986,
                    "delivery3": 5912,
                    "delivery4": 11037,
                    "delivery5": 11099,
                  }
    actime = GamsParameter(db, "actime", 1, "accumulated time spend on driving and picking up")
    for t in actime_data:
        actime.add_record(t).value = actime_data[t]

    due_data = { "delivery1": 1394755200,
                 "delivery2": 1394756086,
                 "delivery3": 1394757063,
                 "delivery4": 1394762400,
                 "delivery5": 1394762400,
               }
    due = GamsParameter(db, "due", 1, "due timestamp")
    for d in due_data:
        due.add_record(d).value = due_data[d]

    start = GamsParameter(db, "start", 0, "timestamp of start time")
    start.add_record().value = 1394748000

    job = GamsJob(ws, source=get_time_error_model())
    opt = GamsOptions(ws)

    opt.defines["gdxincname"] = db.name
    opt.all_model_types = "xpress"

    job.run(opt, databases = db)
    print_results_minimize_time_error(job)



if __name__ == "__main__":
    test()
