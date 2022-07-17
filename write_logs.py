import syslog

def write_syslog(facility = syslog.LOG_INFO,msg):
    syslog.syslog(facility, msg)