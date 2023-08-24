'''
File: gurobi_model.py
Project: Job Orchestration
Description:
-----------
simulator for the solution
-----------
Author: 626
Created Date: 2023-0704
'''

def simulator_utils(solu_t, tasks):
    """
        input the solution of start time and the infomation of tasks
        ouput the resource load of each-time and the parallelism of each-time
    """
    resource_list = []
    parallelism_list = []
    for i in range(1440):
        cur_resource = 0
        cur_parallelism = 0
        for j in range(len(solu_t)):
            if solu_t[j] <= i and (solu_t[j] + tasks[j]["execution_time"]) > i:
                cur_resource += tasks[j]["resource_load"]
                cur_parallelism += 1
        resource_list.append(cur_resource)
        parallelism_list.append(cur_parallelism)

    return resource_list, parallelism_list


 