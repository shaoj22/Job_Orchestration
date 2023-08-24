'''
File: heuristic_OLB.py
Project: Job Orchestration
Description:
-----------
Body code of the OLB heuristic algorithm for job orchestration problem
    · __init__ : init the heuristic OLB
    · iter_optimization : run the heuristic OLB for many times to get the best solution
    · run_OLB : run the heuristic OLB for only once with the given resource cap
    · task_assignmen : at the time of time_now, get the task list that can be inserted
    · calculate_pretasks : calculate whether all pretasks of task have been finished
    · calculate_pretasks_list : calculate the pretasks list of each task
    · calculate_resource_lower_bound : calculate the resource lower bound of the problem
-----------
Author: 626
Created Date: 2023-0706
'''
import copy
import sys
import numpy as np
import time 
import pandas as pd
sys.path.append("..")
from utils import draw_utils
from utils import random_careat_data
from utils import instances
from utils import simulator_utils
from utils import solution_check_utils
from utils import results_export_utils

class heuristic_OLB():
    def __init__(self, instance):
        """
        init the heuristic OLB 从算例中初始化参数
        Args:
            task_num (int): 任务的个数
            tasks (list): 任务的信息
            task_denpendency (list): 任务的依赖关系
            time_cap (int): 规划时间的上限
            resource_cap (float): 资源负载的上限
            resource_gap (float): 资源负载迭代的gap
            accept_resource_gap (float): 资源负载最终结果可接受的误差
            pretasks_list (list): 任务的前置任务  
            resource_lower_bound (float): 资源负载的下界
        """
        self.task_num = instance.task_num
        self.tasks = instance.tasks
        self.task_denpendency = instance.task_denpendency
        self.time_cap = 1440
        self.resource_cap = 1
        self.resource_gap = 1.2
        self.accept_resource_gap = 0.01
        self.pretasks_list = self.calculate_pretasks_list()
        self.resource_lower_bound = self.calculate_resource_lower_bound()

    def iter_optimization(self):
        """
        iter_optimization 迭代优化
        run the heuristic OLB for many times to get the best solution
        """
        resource_gap = self.resource_gap # 当前迭代的资源负载的gap
        upper_bound = self.resource_cap # 当前迭代的资源负载的上界
        while resource_gap >= self.accept_resource_gap: # 当gap小于可接受误差时，停止迭代
            if upper_bound > resource_gap and upper_bound - resource_gap > self.resource_lower_bound:
                solu_t, scheduling_tasks, end_time_mistake_num = self.run_OLB(upper_bound - resource_gap) # 运行OLB算法)
                if len(scheduling_tasks) == 0 and end_time_mistake_num == 0:
                # if len(scheduling_tasks) == 0:
                    solution_t = solu_t # 更新最优解
                    upper_bound = upper_bound - resource_gap # 更新上界
                    end_bound = upper_bound # 更新最终解
                    if resource_gap != self.resource_gap:
                        resource_gap = resource_gap/2
                else:
                    resource_gap = resource_gap/2
            else:
                resource_gap = resource_gap/2

        return solution_t, end_bound
                
    def run_OLB(self, resource_cap):
        """
        runner for OBL heuristic algorithm, just running for once   
        Args:
            resource_cap (float): 当前输入的资源负载的上限 
        """
        end_time_mistake_num = 0 # 任务结束时间误差的个数
        solu_t = [0 for i in range(len(self.tasks))] # 初始化每个任务的开始执行时间
        scheduled_tasks = [] # 已经执行过的任务
        scheduling_tasks = [] # 正在执行的任务
        unscheduled_tasks = [i for i in range(len(self.tasks))] # 未执行的任务
        resource_now = 0 # 当前的资源负载
        for time_now in range(self.time_cap): # 新的time_now到来，更新此时的scheduling_tasks和resource_now
            check_list = copy.copy(scheduling_tasks)
            for i in range(len(check_list)): # update scheduling_tasks
                if time_now >= solu_t[check_list[i]] + self.tasks[check_list[i]]["execution_time"]:
                    scheduling_tasks.remove(check_list[i])
                    scheduled_tasks.append(check_list[i])
                    resource_now -= self.tasks[check_list[i]]["resource_load"]
            # 获取time_now插入的任务列表
            insert_tasks_list, unscheduled_tasks = self.task_assignment(time_now, unscheduled_tasks, resource_now, resource_cap, scheduled_tasks)
            if time_now < self.time_cap - 1:
                for i in range(len(insert_tasks_list)): # 更新solu_t和unscheduled_tasks
                    solu_t[insert_tasks_list[i]] = time_now
                    if self.tasks[insert_tasks_list[i]]["lastest_start_time"] < solu_t[insert_tasks_list[i]]:
                        end_time_mistake_num += 1
                        # print(self.tasks[insert_tasks_list[i]]["task_name"])
                    scheduling_tasks.append(insert_tasks_list[i])
                    resource_now += self.tasks[insert_tasks_list[i]]["resource_load"]
                # print("time now =", time_now, "resource_now =", resource_now, "scheduling_task_num =", len(scheduling_tasks), "scheduled_task_num =", len(scheduled_tasks), "unscheduled_task_num =", len(unscheduled_tasks), "resource_upper_bound =", resource_cap)
            else:
                print("OLB_heuristic_finished")

        return solu_t, scheduling_tasks, end_time_mistake_num

    def task_assignment(self, time_now, unscheduled_tasks, resource_now, resource_cap, scheduled_tasks):
        """
        at the time of time_now, get the task list that can be inserted
        Args:
            time_now (int): 当前时间
            unscheduled_tasks (list): 未执行的任务
            resource_now (float): 当前的资源负载
            resource_cap (float): 当前输入的资源负载的上限
            scheduled_tasks (list): 已经执行过的任务
        """
        ready_list = [] # 可以开始执行的任务
        insert_tasks_list = [] # 可以插入的任务
        ready_task_lastest_start_time_list = [] # 可以插入的任务的最晚开始时间列表
        for i in range(len(unscheduled_tasks)): # 获取ready_list
            if self.tasks[unscheduled_tasks[i]]["earliest_time"] <= time_now and self.calculate_pretasks(scheduled_tasks, unscheduled_tasks[i]) == 1:
                ready_list.append(unscheduled_tasks[i])
                ready_task_lastest_start_time_list.append(self.tasks[unscheduled_tasks[i]]["lastest_start_time"])
        # print(time_now, "-------", ready_list)
        while len(ready_list) != 0: # 获取insert_tasks_list
            ready_task_lastest_start_time = min(ready_task_lastest_start_time_list)
            ready_index = ready_task_lastest_start_time_list.index(ready_task_lastest_start_time)
            insert_task = ready_list[ready_index]
            resource_now += self.tasks[insert_task]["resource_load"]
            if resource_now >= resource_cap: # 若加入后资源会超过上限，则不加入
                break
            else: # 若加入后资源不会超过上限，则加入
                insert_tasks_list.append(insert_task)
                unscheduled_tasks.remove(insert_task)
                ready_list.remove(insert_task)
                ready_task_lastest_start_time_list.remove(ready_task_lastest_start_time)
            
        return insert_tasks_list, unscheduled_tasks

    def calculate_pretasks(self, scheduled_tasks, task):
        """
        calculate whether all pretasks of task have been finished
        Args:
            scheduled_tasks (list): 已经执行过的任务
            task (int): 当前任务
        """
        pretasks_finished_or_not = 1 # 任务所有的前置任务是否都已完成，若是则为1，否则为0
        for i in range(len(self.pretasks_list[task])):
            if self.pretasks_list[task][i] not in scheduled_tasks:
                pretasks_finished_or_not = 0
                break
        
        return pretasks_finished_or_not

    def calculate_pretasks_list(self):  
        """
        calculate all tasks's pretasks
        input tasks information
        output pretasks → a list  
        """
        pretasks_list = [] # 所有任务的前置任务list
        for i in range(self.task_num):
            each_pretasks_list = [] # 每个任务的前置任务list
            for j in range(self.task_num):
                if self.task_denpendency[j][i] == 1: # j是i的前置任务
                    each_pretasks_list.append(j)
            pretasks_list.append(each_pretasks_list)
        
        return pretasks_list

    def calculate_resource_lower_bound(self):
        """
        calculate resource lower bound
        input tasks information
        output resource lower bound → a int 
        """
        resource_sum = 0
        for i in range(self.task_num):
            resource_sum += self.tasks[i]["resource_load"] * self.tasks[i]["execution_time"]

        return resource_sum/1440

if __name__ == "__main__":
    # create data
    tasks_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\utils\\tasks.csv")
    tasks_denpendency_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\utils\\tasks_denpendency.csv")
    tasks_matrix = tasks_df.values.tolist()
    tasks_denpendency = tasks_denpendency_df.values.tolist()
    tasks = []
    task_num = len(tasks_df)
    for i in range(task_num):
        node = tasks_matrix[i][0]
        task_name = tasks_matrix[i][1]
        execution_time = tasks_matrix[i][2]
        resource_load = tasks_matrix[i][3]
        earliest_time = tasks_matrix[i][4]
        latest_time = tasks_matrix[i][5]
        task = {
                    "task No.":node, # 任务编号
                    "task_name": task_name,
                    "earliest_time":earliest_time, # 任务最早完成时间
                    "latest_time":latest_time, # 任务最晚完成时间
                    "execution_time":execution_time, # 任务的持续时间
                    "resource_load":resource_load, # 任务的资源负载
                    "lastest_start_time":latest_time-execution_time, # 任务的最晚开始时间
                }
        tasks.append(task)
    # create instance
    test_instance = instances.instance(task_num, tasks, tasks_denpendency)
    algorithm_tool = heuristic_OLB(test_instance)
    # run OLB heuristic algorithem
    solution_t, resource = algorithm_tool.iter_optimization()
    resource_list, parallelism_list = simulator_utils.simulator_utils(solution_t, test_instance.tasks)
    plt_tool = draw_utils.draw_utils()
    task_names = [i for i in range(task_num)]
    execution_time = []
    for i in range(test_instance.task_num):
        execution_time.append(test_instance.tasks[i]["execution_time"])
    plt_tool.draw_gantt_chart(solution_t, execution_time, task_names)
    plt_tool.draw_resource_line_chart(resource_list)
    plt_tool.draw_parallelism_line_chart(parallelism_list)
    # check the solution
    check_tools = solution_check_utils.solution_check_utils()
    check_tools.solution_check(test_instance.tasks, solution_t, test_instance.task_denpendency)
    

