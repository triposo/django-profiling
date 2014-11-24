# -*- coding: utf-8 -*-
import GreenletProfiler
from datetime import datetime
import os, errno
import logging
import tempfile

tempdir = tempfile.gettempdir()

log = logging.getLogger('profiling')

class InstrumentMiddleware(object):
    
    def process_request(self, request):
        # ignore media
        if self._is_path_ignoreable(request, ['/media', '/static']):
            return
        if not hasattr(request, 'session'):
            print 'request has no session, this middleware needs to be after the SessionMiddleware'
            log.warn('request has no session, this middleware needs to be after the SessionMiddleware')
            return

        # activate profiling?
        if 'greenletprofile' in request.GET:
            log.debug("activate profiling")
            request.session['greenletprofile'] = True
        # stop profiling
        if 'greenletprofile-stop' in request.GET and request.session.get('greenletprofile'):
            log.debug("deactivate profiling")
            request.session['greenletprofile'] = False

        if request.session.get('greenletprofile'):
            log.debug("start profiling")
            GreenletProfiler.set_clock_type('cpu')
            GreenletProfiler.start()


    def process_response(self, request, response):
        if not hasattr(request, 'session'):
            return

        # are we in a profiler run
        if request.session.get('greenletprofile'):
            GreenletProfiler.stop()
            # store the output
            tmpfolder = tempfile.tempdir
            tmpfolder = "%s%s%s" % (tmpfolder, os.sep, "profiler")
            try:
                os.makedirs(os.path.normpath(tmpfolder))
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise
            log_filename = ("callgrind.%s-%s" % (request.META['REMOTE_ADDR'], datetime.now())).replace(" ", "_").replace(":", "-")
            location = "%s%s%s" % (tmpfolder, os.sep, log_filename)
            stats = GreenletProfiler.get_func_stats()
            stats.save(log_filename, type='callgrind')
            log.debug("wrote profiling log: %s" % (location))
            log.debug("for request path: %s" % (request.META["PATH_INFO"]))

        # stop the profiler run
        if request.session.get('greenletprofile') == False:
            try:
                del request.session['greenletprofile']
                log.debug("removed profiling from session")
            except KeyError:
                pass

        return response
    
    def _is_path_ignoreable(self, request, ignore_pathes):
        #@TODO: get the media path from the settings
        ignoreable = False
        for ignore_path in ignore_pathes:
            if unicode(request.META['PATH_INFO']).find(ignore_path) == 0:
                ignoreable = True
                break
        return ignoreable  

