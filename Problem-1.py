import time

#Check if this issue is already added to the queue or not
def check_existance(issue, new_issue):
	if issue.count(new_issue) > 0:
		return True
	else:
		return False

#Give current process status to the user
def show_process_details(issue, running, waiting, terminate):
	print("Total issues assigned so far:: ", issue)
	print("Running process Id:: ", running)
	print("Waiting process Id:: ", waiting)
	print("Terminating process Id:: ", terminate)

#If terminating process is ongoing then remove that process from the queue as well as from start and time_taken
#dictionary that store starting time of the process and total execution time for that process.
#Update status of the process '-1'
#Add the process into termination process list
def check_running_process(running, start, time_taken, status, terminate, terminating_issue):
	for i in range(len(running)):
		if running[i] == terminating_issue:
			running.pop(i)
			start.pop(terminating_issue)
			time_taken.pop(terminating_issue)
			status[terminating_issue] = -1
			terminate.append(terminating_issue)
			break
	return [running, start, time_taken, status, terminate]

#If terminating process is a waiting process then remove that process from waiting process list as well as from start 
#and time_taken dictionary that store starting time of the process and total execution time for that process.
#Update status of the process '-1'
#Add the process into termination process list
def check_waiting_process(waiting, start, time_taken, status, terminate, terminating_issue):
	for i in range(len(waiting)):
		if waiting[i] == terminating_issue:
			waiting.pop(i)
			time_taken.pop(terminating_issue)
			status[terminating_issue] = -1
			terminate.append(terminating_issue)
			break
	return [waiting, start, time_taken, status, terminate]

#Check status for the terminating process and update into the corresponding list
def check_for_terminating_issue(running, waiting, start, time_taken, status, terminate, terminating_issue):
	running, start, time_taken, status, terminate = check_running_process(running, start, time_taken, status, terminate, terminating_issue)
	waiting, start, time_taken, status, terminate = check_waiting_process(waiting, start, time_taken, status, terminate, terminating_issue)
	return [running, waiting, start, time_taken, status, terminate]

#If any onging process is found complted then remove that process from the queue and add in completed process list
#to add any waiting process into the queue as well as updates the corresponding lists.
def remove_completed_process_from_queue(status, running, waiting, start, time_taken, completed, waiting_time):
	temp = []
	for i in range(len(running)):
		curr_time = time.time()
		val = start[running[i]] + time_taken[running[i]]
		if(curr_time >= val):
			status[running[i]] = 2
			completed.append(running[i])
			start.pop(running[i])
			time_taken.pop(running[i])
		else:
			waiting_time = min(waiting_time, (start[running[i]] + time_taken[running[i]] - curr_time))
			temp.append(running[i])
	return [temp, status, running, waiting, start, time_taken, completed, waiting_time]

#If any agent is found free at a particular time and there are some process in the waiting list to be executed
#then assign that process to the free agent and updates the corresponding lists.
def add_waiting_process_into_queue(running, waiting, waiting_time, start, status, time_taken, total_agent):
	while len(running) < total_agent:
		if len(waiting) == 0:
			break
		running.append(waiting[0])
		waiting_time += time_taken[waiting[0]]
		curr_time = time.time()
		start[waiting[0]] = curr_time
		status[waiting[0]] = 1
		waiting.pop(0)
	return [running, waiting, waiting_time, start, status, time_taken]

#After getting any new issue if it's found that atleast one of the agent is free then assign the new issue to
#the agent and update the corresponding process status lists.
#If is found that after getting a new issue none of agent is free to take that process then return minimum
#time the new issue need to wait for execution
def new_issue_status(running, total_agent, new_issue, start, status, waiting, waiting_time):
	if len(running) < total_agent:
		running.append(new_issue)
		curr_time = time.time()
		start[new_issue] = curr_time
		status[new_issue] = 1
		print("Total waiting time:: 0")
	else:
		print("Total waiting time:: ", waiting_time)
		status[new_issue] = 0
		waiting.append(new_issue)
	return [running, new_issue, start, status, waiting]

#Check status for any new isuue.
def process_status(new_issue, issue, status, running, waiting, start, time_taken, completed, total_agent):
	if new_issue != None:
		issue.append(new_issue)
		waiting_time = 100
		status[new_issue] = 0
		running, status, running, waiting, start, time_taken, completed, waiting_time = remove_completed_process_from_queue(status, running, waiting, start, time_taken, completed, waiting_time)
		running, waiting, waiting_time, start, status, time_taken = add_waiting_process_into_queue(running, waiting, waiting_time, start, status, time_taken, total_agent)
		running, new_issue, start, status, waiting = new_issue_status(running, total_agent, new_issue, start, status, waiting, waiting_time)
	return [new_issue, issue, status, running, waiting, start, time_taken, completed]

def main():
	total_agent = int(input("Enter Total No of Agent:: "))
	issue = []
	status = {} 	#2 for resolve, 0 for panding, -1 for abandoned, 1 for running
	running = []	#Ongoing process
	waiting = []	#Pending process
	terminate = []	#Terminating process
	completed = []	#Completed process
	time_taken = {}	#Time taken by the process
	start = {}		#Starting time of the process
	while True:
		show_process_details(issue, running, waiting, terminate)
		print("Please Enter the issue::(Don't Enter same issue) ")
		new_issue = input()
		if check_existance(issue, new_issue):
			print("Alert! You have entered pre-existing issue:: ")
		print("Enter the issue that you want to terminate/(preceed/p to continue):: ")
		terminating_issue = input()
		running, waiting, start, time_taken, status, terminate = check_for_terminating_issue(running, waiting, start, time_taken, status, terminate, terminating_issue)
		required_time = int(input("Enter Required Time:: "))
		time_taken[new_issue] = required_time
		new_issue, issue, status, running, waiting, start, time_taken, completed = process_status(new_issue, issue, status, running, waiting, start, time_taken, completed, total_agent)

if __name__ == '__main__':
	main()