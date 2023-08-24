'''
File: instance.py
Project: Job Orchestration
Description:
-----------
Basic information about the project arithmetic, including:
the number of the task
the execution time of the task
the resources consumed by the execution of the task
the earliest and latest completion times of the task
the dependencies of the task
the fixed total number of resources.
-----------
Author: 626
Created Date: 2023-0704
'''
import utils.random_careat_data as random_careat_data


class instance():
    def __init__(self, task_num, tasks, task_denpendency):
        """
        Args:
            R (int): 最大的资源负载固定为1
            task_num (int): 任务的数量
            tasks[i]['execution_time'] (int): 完成每个任务需要的执行时间
            tasks[i]['earliest_time'] (int): 每个任务的最早完成时间
            tasks[i]['latest_time'] (int): 每个任务的最晚完成时间
            tasks[i]['resource_load'] (int)：完成每个任务需要的资源负载
            task_denpendency (0-1): 二维列表：任务之间是否存在依赖关系
            tasks : 二维列表：存储任务的所有信息
        """
        self.R = 1
        self.task_num = task_num
        self.tasks = tasks
        self.task_denpendency = task_denpendency

if __name__ == "__main__":
    num = 10
    # create data
    test_data = random_careat_data.random_data(num) 
    # get information from data
    task_num = test_data.task_num
    tasks = test_data.tasks
    tasks_denpendency = test_data.task_denpendency
    # create instance
    test_instance = instance(task_num, tasks, tasks_denpendency)