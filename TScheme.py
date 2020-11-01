import win32com.client
import time
import subprocess



class Utils:
    TASK_STATE = {
        0: 'Unknown',
        1: 'Disabled',
        2: 'Queued',
        3: 'Ready',
        4: 'Running'
    }
    TASK_INTERVALS = {
        'hour':3600,
        'day':86400,
        'week':604800,
        'month':2629743,
        'year':31556926,
         '>year':31556927
    }
    TASK_RESULTS = {
        "0":"Runned",
        "1":'1',
        "-2147221164":"-2147221164",
        "268435456":"268435456",
        "-2147020576":"Denied by admin",
        "267009":"Running now!",
        "-2147024891":"Access denied",
        "267011":"Never run"
        }
    def __init__(self):
        pass

    def task_state(self,state):
        "Current state of task"
        if state in self.TASK_STATE:
            return self.TASK_STATE[state]
        return state

    def time_interval(self,task_time):
        "Get interval of which task was performed"
        diff_time = time.time() - task_time
        for interval in list(self.TASK_INTERVALS.items())[:-1]:
            if diff_time <= interval[1]: return interval[0]
        return list(self.TASK_INTERVALS.items())[-1][0]

    def task_result(self,result):
        "Result response from task"
        if str(result) in self.TASK_RESULTS.keys():
            return self.TASK_RESULTS[str(result)]
        else: return str(result)
        
    def index_of_interval(self,interval):
        "Get index of interval"
        return list(self.TASK_INTERVALS.keys()).index(interval)

    def get_rowInfo(self,state=None, run=None, result=None,**kwargs):
        "Modify content to more readable state"
        return self.task_state(state), self.time_interval(run), self.task_result(result)

class Server:
    def __init__(self):
        pass
    
    def connect2Scheduler(self):
        "Connect to scheduler service"
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        return [scheduler.GetFolder('\\')]

    def disable(self,task_path):
        "Disable task"
        subprocess.Popen(['SCHTASKS', '/CHANGE', '/TN', task_path,"/DISABLE"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
    def enable(self,task_path):
        "Enable task"
        subprocess.Popen(['SCHTASKS', '/CHANGE', '/TN', task_path,"/ENABLE"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
class schedule_handler(Server, Utils):
    TASKS = {'info':{}, 'disabled':{}, 'suggested':{}, 'ignored':{}}
    
    def __init__(self):
        Server.__init__(self)
        Utils.__init__(self)

    def __str__(self):
        return """
*** Scheduler ***
This program allow the user to edit all scheduled tasks accessed in windows
By using this program to disable unnecessary tasks it is possible to speed up the computer.

# Note: In order to see all scheduled tasks (NT instance\system) the code need to be run as Administrator

print(category)
    category: info, suggested, disabled, ignored
    
sync(): The program will search for existing tasks and group them into categories:
    SUGGESTED: Contains all task that is suggested or can be disabled.
    INFO:      All the tasks that is found on the scheduler.
    DISABLED:  All the disabled tasks
    IGNORED:   All tasks that has not been used within a year.

find_task(name, path=None)
    Search for a task either by path and/or name. Primary name is used.

find_and_disable(name, path=None, enable=True):
    Search for a task either by path and/or name. Primary name is used. Enable per default

Enable/Disable task:
    disable(task_path), enable(task_path) which expects a path to the task.

"""
    
    def add_INFO(self, name, path,
                      state='Unknown',
                      lastRun=None,
                      lastRunresult=None, **kwargs):
        "Add info to storage"
        self.TASKS['info'].update({path:{}})
        self.TASKS['info'][path].update({name:{'state':state, 'run':lastRun, 'result':lastRunresult}})
        
    def add(self, name, path, category):
        "Add data to storage"
        self.TASKS[category].update({path:[]})
        self.TASKS[category][path].append(name)
        
    def print(self,category):
        "Print based on category, Check __str__() for more info"
        if category == 'info':
            print(f"*** {category} ***\n" + '\n'.join([f'{key:<60}{list(val.keys())[0]}:{self.get_rowInfo(**list(val.values())[0])}' for key, val in self.TASKS[category].items()]))
        else:
            print(f"*** {category} ***\n" + '\n'.join([f'{key:<60}{val}'  for key, val in self.TASKS[category].items()]))
 
        
    def sync(self):
        "Synd data from scheduler"
        folders = self.connect2Scheduler()
        while folders:
            folder, folders = self.get_folder(folders)
            
            for task in folder.GetTasks(1):
                self.get_task(task)

    def get_folder(self, folders):
        "Get all folders from scheduler"
        folder = folders.pop(0)
        folders += list(folder.GetFolders(1))
        return folder, folders

    def get_task(self, task):
        "Get data of task object"
        path, name = task.Path.rsplit("\\",1)
        state = task.State
        lastRun = task.LastRunTime.timestamp()
        lastRunresult = task.LastTaskResult
        
        # Add all tasks
        self.add_INFO(name, path, state, lastRun, lastRunresult)
        
        # Continue if disable
        if state == 1:
            self.add(name,path, 'disabled')
        # Add to suggested removal if last run within the year
        elif self.index_of_interval(self.time_interval(lastRun)) < self.index_of_interval('year'):
            self.add(name,path, 'suggested')
        else:
            self.add(name,path,'ignored')
    
    def find_task(self, name, path=None):
        "Find a task based on name and or path"
        def con_path_name():
            return task_path == path and task_name == name
        def con_name():
            return task_name == name
        
        condition = {
            'both':con_path_name,
            'name':con_name,
        }
        by = 'both' if path != None else 'name'
        folders = self.connect2Scheduler()
        while folders:
            folder, folders = self.get_folder(folders)
            
            for task in folder.GetTasks(1):
                task_path, task_name = task.Path.rsplit("\\",1)
                if condition[by]():
                    return task
            
    def find_and_disable(self, name, path=None, enable=True):
        """enable needs to be False in order to disable, to reduce chance of misstake"""
        task = self.find_task(name, path)

        self.enable(task.Path) if enable==True else self.disable(task.Path)
        
if __name__ == '__main__':
    scheduler = schedule_handler()
    scheduler.sync()
    print(scheduler)
