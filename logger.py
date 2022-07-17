#import logging
import write_logs

#logging.basicConfig(filename='fan.log', encoding='utf-8', level=logging.DEBUG)
#logging.info('test INFO message')
#logging.warning('test WARNING message')

write_logs.write_syslog(syslog.LOG_ERR, "This is a test message....")