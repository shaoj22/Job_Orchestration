'''
File: gurobi_model_experience.py
Project: Job Orchestration
Description:
-----------
using the gurobi model to do some experience for the job orchestration problem
-----------
Author: 626
Created Date: 2023-0727
'''
import sys
sys.path.append("..")
from utils import draw_utils
from utils import random_careat_data
from utils import instances
from utils import simulator_utils
from utils import solution_check_utils
from utils import results_export_utils
from static_job_scheduling_heuristics_algorithem import heuristic_OLB
import gurobi_model
import old_gurobi_model
import time
from utils import data
import pandas as pd

# create data
tasks_df = pd.read_csv("tasks.csv")
tasks_denpendency_df = pd.read_csv("tasks_denpendency.csv")
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
# create gurobi model
# gurobi_model = old_gurobi_model.gurobi_model(test_instance, time_limit=1000)
gurobi_model = gurobi_model.gurobi_model(test_instance, time_limit=14400)
# run gurobi model
OLB_heuristic_algorithem_tool = heuristic_OLB.heuristic_OLB(test_instance)
solution_t, resource = OLB_heuristic_algorithem_tool.iter_optimization()
print("resource_cap:", resource)
result_info = gurobi_model.run_model(solution_t)
# draw the gantt chart
plt_tools = draw_utils.draw_utils()
execution_time = []
for i in range(test_instance.task_num):
    execution_time.append(test_instance.tasks[i]["execution_time"])
plt_tools.draw_gantt_chart(result_info["task_start_time"], execution_time, [i for i in range(task_num)])
resource_list, parallelism_list = simulator_utils.simulator_utils(result_info["task_start_time"], test_instance.tasks)
# draw the resource line chart and parallelism line chart
plt_tools.draw_resource_line_chart(resource_list)
plt_tools.draw_parallelism_line_chart(parallelism_list)
# check the results of OLB heuristic algorithm
check_tools = solution_check_utils.solution_check_utils()
check_tools.solution_check(test_instance.tasks, result_info["task_start_time"], test_instance.task_denpendency)
# export the results of OLB heuristic algorithm into csv file
results_export_utils.results_export_utils(solution_t, test_instance.tasks)
