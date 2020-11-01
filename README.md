# TScheme
TScheme stands for Task Scheduler Modifier. Modify task within task scheduler. Enable and disable and get an overview of tasks within the scheduler to disable unused and  performance demanding tasks.

# So what can it do?

*** Scheduler ***
This program allow the user to edit all scheduled tasks accessed in windows
By using this program to disable unnecessary tasks it is possible to speed up the computer.

*  Note: In order to see all scheduled tasks (NT instance\system) the code need to be run as Administrator

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

# How to use
The run.py file contains an example and doc for TScheme. 
Run $py run.py$

