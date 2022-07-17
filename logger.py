#import logging
import syslog

def write_syslog(facility = syslog.LOG_INFO, msg = "Message not specified"):
    syslog.syslog(facility, msg)

#logging.basicConfig(filename='fan.log', encoding='utf-8', level=logging.DEBUG)
#logging.info('test INFO message')
#logging.warning('test WARNING message')

write_syslog(syslog.LOG_ERR, "This is a test message....")