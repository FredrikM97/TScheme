import win32com.client
import subprocess

def connect2Scheduler():
	"Connect to scheduler service"
	scheduler = win32com.client.Dispatch('Schedule.Service')
	scheduler.Connect()
	return [scheduler.GetFolder('\\')]

def disable(task_path):
	"Disable task"
	subprocess.Popen(['SCHTASKS', '/CHANGE', '/TN', task_path,"/DISABLE"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
def enable(task_path):
	"Enable task"
	subprocess.Popen(['SCHTASKS', '/CHANGE', '/TN', task_path,"/ENABLE"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    