# daemon.py
#import ???
import os
import sys
import atexit
import signal
import logging

#logging.basicConfig(level=logging.INFO, filename='err_log.log', filemode='w')

class Daemon:
	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'): 
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile

	def daemonize(self):
		"""Deamonize class. UNIX double fork mechanism."""
		try:
			pid = os.fork()
			if pid > 0:
				# exit first parent
				sys.exit(0)
		except OSError as err:
			sys.stderr.write('fork #1 failed: {0}\n'.format(err))
			sys.exit(1)

		# decouple from parent environment
		os.chdir('/')
		os.setsid()
		os.umask(0)

		# do second fork
		try:
			pid = os.fork()
			if pid > 0:
				# exit from second parent
				sys.exit(0)
		except OSError as err:
			sys.stderr.write('fork #2 failed: {0}\n'.format(err))
			sys.exit(1)

		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = open(self.stdin, 'r')
		so = open(self.stdout, 'a+')
		se = open(self.stderr, 'a+')

		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())		
		os.dup2(se.fileno(), sys.stderr.fileno())

		# write pidfile
		atexit.register(self.delpid)

		pid = str(os.getpid())
		with open(self.pidfile,'w+') as f:
			f.write(pid + '\n')

	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		# your ode
		if os.path.isfile(self.pidfile):
			if os.path.getsize(self.pidfile) > 0:
				print('скрип уже запущен')
				sys.exit()
		self.daemonize()
		self.run()
	def stop(self):
		# your code
		try:
			f = open(self.pidfile,'r')
			int_pid = int(f.readline().strip().lstrip())
			#logging.info(int_pid)
			self.delpid()
			os.kill(int_pid,signal.SIGTERM)		
		except:
			sys.stderr.write('скрип не запущен')
			sys.exit()

			
	def restart(self):
		"""Restart the daemon."""
		self.stop()
		self.start()

	def run(self):
		pass
	"""You should override this method when you subclass Daemon."""
	"""It will be called after the process has been daemonized by"""
	"""start() or restart()."""

