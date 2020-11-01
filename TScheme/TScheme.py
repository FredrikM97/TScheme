from .server import connect2Scheduler, disable, enable
from .utils import get_rowInfo, index_of_interval,time_interval

class TScheme:
    TASKS = {'info':{}, 'disabled':{}, 'suggested':{}, 'ignored':{}}
    
    def __init__(self):
        pass
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
            print(f"*** {category} ***\n" + '\n'.join([f'{key:<60}{list(val.keys())[0]}:{get_rowInfo(**list(val.values())[0])}' for key, val in self.TASKS[category].items()]))
        else:
            print(f"*** {category} ***\n" + '\n'.join([f'{key:<60}{val}'  for key, val in self.TASKS[category].items()]))
 
        
    def sync(self,**kwargs):
        "Synd data from scheduler"
        folders = connect2Scheduler()
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
        elif index_of_interval(time_interval(lastRun)) < index_of_interval('year'):
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
        folders = connect2Scheduler()
        while folders:
            folder, folders = self.get_folder(folders)
            
            for task in folder.GetTasks(1):
                task_path, task_name = task.Path.rsplit("\\",1)
                if condition[by]():
                    return task
            
    def find_and_disable(self, name, path=None, enable=True):
        """enable needs to be False in order to disable, to reduce chance of misstake"""
        task = self.find_task(name, path)

        enable(task.Path) if enable==True else disable(task.Path)
