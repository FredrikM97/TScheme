import time

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
	
def task_state(state):
	"Current state of task"
	if state in TASK_STATE:
		return TASK_STATE[state]
	return state

def time_interval(task_time):
	"Get interval of which task was performed"
	diff_time = time.time() - task_time
	for interval in list(TASK_INTERVALS.items())[:-1]:
		if diff_time <= interval[1]: return interval[0]
	return list(TASK_INTERVALS.items())[-1][0]

def task_result(result):
	"Result response from task"
	if str(result) in TASK_RESULTS.keys():
		return TASK_RESULTS[str(result)]
	else: return str(result)
	
def index_of_interval(interval):
	"Get index of interval"
	return list(TASK_INTERVALS.keys()).index(interval)

def get_rowInfo(state=None, run=None, result=None,**kwargs):
	"Modify content to more readable state"
	return task_state(state), time_interval(run), task_result(result)