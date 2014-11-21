This fork supports GreenletProfiler_ instead of cProfile. Useful if you run Django with gevent.

Profiling
---------
Your Django became too slow?

Install
========
add this to your settings.py

	INSTALLED_APPS += ['profiling']
	MIDDLEWARE_CLASSES += ['profiling.middleware.InstrumentMiddleware']

	pip install GreenletProfiler

How to do a profiling run
--------------------------
	add a get param: "greenletprofile" to start profiling

	add a get param: "greenletprofile-stop" to stop profiling
 
	the log will be in the tmp/profiler folder of your system


Inspired by
----------- 
	http://lurkingideas.net/profiling-django-projects-cachegrind/


CacheGrinder
------------
	pyprof2calltree -i logfilename.pro -k

	or

	pyprof2calltree -i logfilename.pro -o callgrinder.logfilename.log


additional Profiling Resources:
-------------------------------
	TBD

.. _GreenletProfiler: http://greenletprofiler.readthedocs.org/en/latest/

