'''
File: real_time_algorithem.py
Project: Job Orchestration
Description:
-----------
real_time scheduling algorithem main for job orchestration problem
-----------
Author: 626
Created Date: 2023-0713
'''
import utils.random_careat_data as random_careat_data
import simulator
import utils
import utils.instances as instances
import time
import utils.heuristic_OLB as heuristic_OLB
import copy


class real_time_algorithem():
    def __init__(self, tasks, task_num, task_denpendency, solution_t):
        """
        input instance: task_num, tasks, task_denpendency
        output solu_t    
        """
        self.tasks = tasks # 已经规划过的任务的基本信息
        self.task_num = task_num # 已经规划过的任务的数量 
        self.tasks_denpendency = task_denpendency # 已经规划过后的任务的依赖关系
        self.solution_t = solution_t
    def run(self):
        """
        runner(main process) for the real_time_algorithem   
        """
        self.find_dependent_tasks()
        print(self.change_tasks)
        pass
  
    def find_dependent_tasks(self):
        unchecked_list = copy.deepcopy(self.change_tasks) # 未检查的任务列表
        checked_list = [] # 已检查的任务列表
        while len(unchecked_list) != 0:
            print(unchecked_list)
            for i in range(self.task_num):
                if (self.tasks_denpendency[unchecked_list[0]][i] == 1 or self.tasks_denpendency[i][unchecked_list[0]] == 1) and i not in checked_list and i not in unchecked_list:
                    unchecked_list.append(i)
                    self.change_tasks.append(i)
            checked_list.append(unchecked_list[0])
            unchecked_list.remove(unchecked_list[0])

    def reschedule_tasks(self):
        # for i in range(self.change_tasks):

        pass

    def add_tasks(self, add_tasks):
        """
        input add_tasks
        output those tasks's scheduled start time   
        """
        tasks_start_time_list = []  # create time list for add tasks
        new_tasks = copy.deepcopy(self.tasks) # create new tasks
        for i in range(len(add_tasks)): # calculate new start time 
            new_tasks.append(add_tasks[i])
            task_start_time = add_tasks[i]["latest_time"] - add_tasks[i]["execution_time"]
            tasks_start_time_list.append(task_start_time)

        return tasks_start_time_list, new_tasks

    def modify_tasks(self):
        pass

if __name__ == "__main__":
    task_num = 1000 # 任务的数量
    # create data
    test_data = random_careat_data.random_data(task_num) 
    # get information from data
    task_num = test_data.task_num
    tasks = test_data.tasks
    tasks_denpendency = test_data.task_denpendency
    # create instance
    test_instance = instances.instance(task_num, tasks, tasks_denpendency)
    # create OLB heuristic algorithem
    OLB_heuristic_algorithem_tool = heuristic_OLB.heuristic_OLB(test_instance)
    # run OLB heuristic algorithem
    start_time = time.time()
    solution_t = OLB_heuristic_algorithem_tool.iter_optimization()
    end_time = time.time()
    # draw 
    plt_tools = utils.utils()
    execution_time = []
    for i in range(test_instance.task_num):
        execution_time.append(test_instance.tasks[i]["execution_time"])
    # plt_tools.draw_gantt_chart(solution_t,execution_time)
    resource_list = simulator.simulator(solution_t, test_instance.tasks)
    # 绘制结果柱状图
    plt_tools.draw_bar_chart(resource_list)
    # create real_time algorithem
    real_time_algorithem_tool = real_time_algorithem(test_instance.tasks, test_instance.task_num, test_instance.task_denpendency, solution_t)
    add_data = random_careat_data.random_data(1000)
    # get information from data
    add_task_num = add_data.task_num
    add_tasks = add_data.tasks
    add_tasks_denpendency = add_data.task_denpendency
    # create instance
    add_instance = instances.instance(add_task_num, add_tasks, add_tasks_denpendency)
    add_start_time = time.time()
    add_start_time_list, new_tasks = real_time_algorithem_tool.add_tasks(add_tasks)
    add_end_time = time.time()
    print(add_start_time_list)
    print("add_tasks_cost_time:", add_end_time - add_start_time)
    for i in range(add_task_num):
        solution_t.append(add_start_time_list[i])
    # draw 
    execution_time = []
    for i in range(len(new_tasks)):
        execution_time.append(new_tasks[i]["execution_time"])
    # plt_tools.draw_gantt_chart(solution_t,execution_time)
    resource_list = simulator.simulator(solution_t, new_tasks)
    # 绘制结果柱状图
    plt_tools.draw_bar_chart(resource_list)
    

