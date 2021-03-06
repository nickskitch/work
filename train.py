__author__ = 'Nick'
import os
import subprocess
import time
import library

from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

minutesOfNotice=7
minutesOfLastNotice=5

debugFile=open("/tmp/train.py.log", "a")
debugFile.writelines("\nstarted at " + str(datetime.now()))

times = ("1500","1600","1700", "1800", "1900","2100")
departData = []
depart = []
debug = None
debug = True


debugFile.writelines("\nbefore curl " + str(datetime.now()))
print depart


for t in times:
    cmd2 = "curl -s 'http://www.bart.gov/schedules/bystationresults?station=MONT&date=today&time=" + t + "' | grep Millbrae | awk '{gsub(/<[^>]+>/,\"\");print $1}'"
    print cmd2
    departData.append(subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip())

debugFile.writelines("\nafter curl " + str(datetime.now()))


for d in departData:
    depart.extend(d.split('\n'))


while True:
    debugFile.writelines("\nin loop " + str(datetime.now()))

    for d in depart:
        str2=time.strftime("%b %d %Y ") +d.strip()+'PM'
        bartdepart_dateObject = parser.parse(str2)
        if debug: print 'comparing ' + str(bartdepart_dateObject) + ' to ' + str(datetime.now())
        minsFromNow_dateObject = (datetime.now() + timedelta(minutes=minutesOfNotice))
        if bartdepart_dateObject >= datetime.now():
            rd = relativedelta(bartdepart_dateObject,datetime.now())

            if debug: print "yes, comparing " + str(bartdepart_dateObject) + " <= to " + str(minsFromNow_dateObject)
            if bartdepart_dateObject <= minsFromNow_dateObject:
                message = "train departs in %(minutes)d" % rd.__dict__ + " minutes: " + bartdepart_dateObject.strftime('%I:%M%p')
                if debug: print message
                if bartdepart_dateObject >= (datetime.now() + timedelta(minutes=minutesOfLastNotice)):
                    killcommand = "kill -9 "+str(os.getpid());

                    cmd2 = "terminal-notifier -message '" + str(message) + "' -execute '"+killcommand + "'"
                    print cmd2
                    subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
                    break
            else:
                print "Next depart is in %(minutes)d minutes at " % rd.__dict__ +d.strip()+'PM'
                break

    debugFile.writelines("\nbefore ispingable " + str(datetime.now()))
    try:
        debugFile.writelines(library.isPingable('google.com') + str(datetime.now()))

        # exit the script if I'm not at work
        if library.isPingable('google.com'):
            if not library.isPingable('confluence'):
                if not library.isPingable('jira'):
                    print 'you''re not at work; exiting'
                    exit()
    except:
        debugFile.writelines('error when pinging' + str(datetime.now()))

    debugFile.writelines("\nafter ispingable " + str(datetime.now()))

    time.sleep(60)

debugFile.close()

