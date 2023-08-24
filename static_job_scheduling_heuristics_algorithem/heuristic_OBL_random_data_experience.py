'''
File: heuristic_OLB_random_data_experience.py
Project: Job Orchestration
Description:
-----------
using the OLB heuristic algorithem to do some random data experience for the job orchestration problem
-----------
Author: 626
Created Date: 2023-0718
'''
import sys
sys.path.append("..")
from utils import instances
from utils import solution_check_utils
from utils import results_export_utils
import heuristic_OLB
import time
import pandas as pd

Instances_results = []
for num in range(1,16):
    # create data
    tasks_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\utils\\Instances\\Job_Scheduling_Table_{}.csv".format(num))
    tasks_denpendency_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\utils\\Instances\\Task_Dependency_Table_{}.csv".format(num))
    tasks_matrix = tasks_df.values.tolist()
    tasks_denpendency = tasks_denpendency_df.values.tolist()
    tasks = []
    task_num = len(tasks_df)
    for i in range(len(tasks_matrix)):
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
    # create OLB heuristic algorithem
    OLB_heuristic_algorithem_tool = heuristic_OLB.heuristic_OLB(test_instance)
    # run OLB heuristic algorithem
    start_time = time.time()
    solution_t, resource = OLB_heuristic_algorithem_tool.iter_optimization()
    end_time = time.time()
    # check solution
    check_tools = solution_check_utils.solution_check_utils()
    check_tools.solution_check(test_instance.tasks, solution_t, test_instance.task_denpendency)
    # export results
    results_export_utils.results_export_utils(solution_t, test_instance.tasks, num)
    Instances_results_one = []
    Instances_results_one.append(num)
    Instances_results_one.append(task_num)
    Instances_results_one.append(round(end_time-start_time, 4))
    Instances_results_one.append(round(resource, 4))    
    Instances_results.append(Instances_results_one)

colunms = ["Instance No.", "task_num", "Total time", "Total resource"]
instances_df = pd.DataFrame(Instances_results, columns=colunms)
instances_df.to_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\utils\\Instances_results.csv", index=False)
