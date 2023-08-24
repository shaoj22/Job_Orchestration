'''
File: solution_check_utils.py
Project: Job Orchestration
Description:
-----------
utils for the job orchestration, such as plt tools
-----------
Author: 626
Created Date: 2023-0719
'''
class solution_check_utils():
    def solution_check(self, tasks, solu_t, tasks_dependency):
        """
            check the solution is feasible or not
        """
        # check the start time is feasible or not
        i1 = 0
        for i in range(len(solu_t)):
            if solu_t[i] < tasks[i]["earliest_time"]:
                i1 += 1
                print("start time mistakes:", False, i1)
        print("solution check: start time is feasible")
        # check the end time is feasible or not
        j = 0
        for i in range(len(solu_t)):
            if solu_t[i] + tasks[i]["execution_time"] > tasks[i]["latest_time"]:
                j += 1
                print ("task", i, "end time mistakes:", False, j , "complete time:", solu_t[i] + tasks[i]["execution_time"], "lastset time:", tasks[i]["latest_time"])
        print("solution check: end time is feasible")
        # check the pretask is feasible or not
        k = 0
        pretasks_list = self.calculate_pretasks_list(len(solu_t), tasks_dependency)
        for i in range(len(solu_t)):
            for j in range(len(pretasks_list[i])):
                if solu_t[i] < solu_t[pretasks_list[i][j]] + tasks[pretasks_list[i][j]]["execution_time"]:
                    k += 1
                    print ("pretask mistakes:", False, k)
        print("solution check: pretask is feasible")
                
    def calculate_pretasks_list(self, task_num, task_denpendency):
        """
        a 2D list for each tasks's pretasks
        """
        pretasks_list = [] # 所有任务的前置任务list
        for i in range(task_num):
            each_pretasks_list = [] # 每个任务的前置任务list
            for j in range(task_num):
                if task_denpendency[j][i] == 1: # j是i的前置任务
                    each_pretasks_list.append(j)
            pretasks_list.append(each_pretasks_list)
            # print("calculate the pretasks:", "task num =", i, "pretasks:", each_pretasks_list)
        
        return pretasks_list

    def tasks_priority_cheack(self, tasks, task_priority, task_dependency):
        """
        check the priority is feasible or not
        """
        for i in range(len(task_priority)):
            for j in range(i, len(task_priority)):
                if task_dependency[task_priority[j]][task_priority[i]] == 1:
                    print ("tasks_denpendency mistakes:", False)
                print(tasks[task_priority[j]]["latest_time"], tasks[task_priority[j]]["execution_time"], tasks[task_priority[i]]["latest_time"], tasks[task_priority[i]]["execution_time"])
                if tasks[task_priority[j]]["latest_time"] - tasks[task_priority[j]]["execution_time"] < tasks[task_priority[i]]["latest_time"] - tasks[task_priority[i]]["execution_time"]:
                    print ("tasks_time mistakes:", False)