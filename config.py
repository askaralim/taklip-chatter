# gunicorn.py
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

loglevel = 'info'
# debug = True
bind = '127.0.0.1:5000'
timeout = 30
# worker_class = 'gevent'

accesslog = "/var/tmp/gunicorn_access.log"
errorlog = "/var/tmp/gunicorn_error.log" 
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

daemon = True

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2