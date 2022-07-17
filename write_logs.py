import syslog

def write_syslog(facility = syslog.LOG_INFO,msg = "Message not specified"):
    syslog.syslog(facility, msg)