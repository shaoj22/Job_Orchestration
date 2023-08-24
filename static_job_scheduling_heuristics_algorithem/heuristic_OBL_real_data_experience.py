'''
File: heuristic_OLB_real_data_experience.py
Project: Job Orchestration
Description:
-----------
using the OLB heuristic algorithem to do some real data experience for the job orchestration problem
-----------
Author: 626
Created Date: 2023-0718
'''
import sys
sys.path.append("..")
from utils import draw_utils
from utils import random_careat_data
from utils import instances
from utils import simulator_utils
from utils import solution_check_utils
from utils import results_export_utils
from utils import draw_link_graph
import heuristic_OLB
import time
from utils import data
import pandas as pd

# create data
tasks_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\Job_Scheduling_CDOP(non-ms).csv")
tasks_denpendency_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\Tasks_Denpendency_CDOP(non-ms).csv")
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
# solution_t, scheduling_tasks, end_time_mistake_num = OLB_heuristic_algorithem_tool.run_OLB(1)
end_time = time.time()
# print("tasks_start_time:", solution_t)
# print("resource_cap:", resource)
print("time_cost:", end_time - start_time)
# draw the gantt chart 
plt_tools = draw_utils.draw_utils()
execution_time = []
for i in range(test_instance.task_num):
    execution_time.append(test_instance.tasks[i]["execution_time"])
task_names = [i for i in range(task_num)]
# plt_tools.draw_gantt_chart(solution_t, execution_time, task_names)
# draw the resource load chart
resource_list, parallelism_list = simulator_utils.simulator_utils(solution_t, test_instance.tasks)
rounded_list = [round(num, 5) for num in resource_list]
# plt_tools.draw_resource_line_chart(rounded_list)
# a = pd.DataFrame(rounded_list)
# a.to_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\resource.csv")
# plt_tools.draw_parallelism_line_chart(parallelism_list)
# check the solution
# check_tools = solution_check_utils.solution_check_utils()
# check_tools.solution_check(test_instance.tasks, solution_t, test_instance.task_denpendency)
# export the results of OLB heuristic algorithm into csv file
# results_export_utils.results_export_utils(solution_t, test_instance.tasks, 'cdop')
names = []
for i in range(len(tasks_matrix)):
    name = tasks_matrix[i][1] + " : " + str(solution_t[i])
    names.append(name)
# draw_link_graph.draw_dag_with_dependency_chains(tasks_denpendency, names, solution_t)
chain_groups = draw_link_graph.draw_dag_from_matrix_with_dynamic_ranges(tasks_denpendency, names, solution_t)