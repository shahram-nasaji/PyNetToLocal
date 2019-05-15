from ConfigStructure import Config
from ConfigClasses import ConfigSvc
from DirectoryClasses import DirectorySvc
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import datetime

class NetToLocalSvc(win32serviceutil.ServiceFramework):
	_svc_name_ = "NetToLocalSvc"
	_svc_display_name_ = "NetToLocal Copy Service"
	_svc_description_ = "Python service used to copy downloaded files from internet to a local server"

	def __init__(self,args):
		win32serviceutil.ServiceFramework.__init__(self,args)
		self.hWaitStop = win32event.CreateEvent(None,0,0,None)
		socket.setdefaulttimeout(60)  

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		win32event.SetEvent(self.hWaitStop)

	def SvcDoRun(self):  
		##servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_,''))
		config_service = ConfigSvc("C:\\Users\\sh.akbari\\Desktop\\PythonSvc\\app.config")
		source_node = config_service.get_source_path()
		destination_node = config_service.get_destination_path()

		log_file = open('c:\\svc_log.dat', 'w+')  
		rc = None  

		directory_service = DirectorySvc()

		# if the stop event hasn't been fired keep looping  
		while rc != win32event.WAIT_OBJECT_0:  
			directory_service.replicate_directories(source_node.url, destination_node.url)

			log_file.write('Replication done at ' + str(datetime.datetime.now()) + ' \n')  
			log_file.flush()
			
			# block for 5 seconds and listen for a stop event  
			rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)

		log_file.write('SHUTTING DOWN\n')  
		log_file.close() 

if (__name__ == '__main__'):
	win32serviceutil.HandleCommandLine(NetToLocalSvc) 