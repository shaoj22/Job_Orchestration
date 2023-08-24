import pandas as pd
import numpy as np
import re
import tqdm
# def add_indirect_reachability(matrix):
#     n = len(matrix)
#     closure = [[0 for _ in range(n)] for _ in range(n)]

#     for i in range(n):
#         for j in range(n):
#             closure[i][j] = matrix[i][j]

#     for k in range(n):
#         for i in range(n):
#             for j in range(n):
#                 closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])

#     return closure
# tasks_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\result_pzy.csv")
# tasks_denpendency = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\utils\\Appendix_2_Tasks_Denpendency.csv")
# tasks_denpendency = add_indirect_reachability(tasks_denpendency)
# # 行和
# tasks_denpendency_row_sum = tasks_denpendency.sum(axis=1)
# # 列和
# tasks_denpendency_col_sum = tasks_denpendency.sum(axis=0)
# row_sum = 0
# col_sum = 0
# double_sum = 0
# start_node_1 = []
# end_node_1 = []
# for i in range(len(tasks_denpendency_row_sum)):
#     if tasks_denpendency_row_sum[i] == 0:
#         row_sum += 1
#         end_node_1.append(i)
#     if tasks_denpendency_col_sum[i] == 0:
#         col_sum += 1
#         start_node_1.append(i)
#     if tasks_denpendency_row_sum[i] == 0 and tasks_denpendency_col_sum[i] == 0:
#         double_sum += 1
# for i in range(len(end_node_1)):
#     for j in range(len(tasks_denpendency)):
#         if tasks_denpendency[end_node_1[i]][j] == 1:
#             print(False)
# print("start_num", col_sum)
# print("end_num", row_sum)
# print("start_end_num", double_sum)

# tasks_df = tasks_df.values.tolist()
# task_info = {}
# tasks = []
# for i in range(len(tasks_df)):
#     task_info = {
#         "task No.":tasks_df[i][0] - 1, # 任务编号
#         "task_name": tasks_df[i][1], # 任务名称
#         "pre_task": tasks_df[i][2], # 前置任务
#     }
#     tasks.append(task_info)
# start_node = 0
# for i in range(len(tasks)):
#     if tasks[i]["pre_task"] is np.nan:
#         start_node += 1
# # 前置任务
# pre_task = []
# for i in range(len(tasks)):
#     s = str(tasks[i]["pre_task"])
#     numbers = re.findall(r'\d+', s)
#     number_list = [int(num) for num in numbers]
#     pre_task.append(number_list)

    

# # 依赖矩阵
# tasks_dependency = np.zeros((len(tasks), len(tasks)))
# for i in range(len(tasks)):
#     for j in range(len(tasks)):
#         if j in pre_task[i]:
#             tasks_dependency[j][i] = 1
#         else:
#             tasks_dependency[j][i] = 0
# # tasks_dependency = add_indirect_reachability(tasks_dependency)
# # 行和
# tasks_denpendency_row_sum = tasks_dependency.sum(axis=1)
# # 列和
# tasks_denpendency_col_sum = tasks_dependency.sum(axis=0)
# row_sum = 0
# col_sum = 0
# double_sum = 0
# start_node_1 = []
# end_node_1 = []
# for i in range(len(tasks_denpendency_row_sum)):
#     if tasks_denpendency_row_sum[i] == 0:
#         row_sum += 1
#         end_node_1.append(i)
#     if tasks_denpendency_col_sum[i] == 0:
#         col_sum += 1
#         start_node_1.append(i)
#     if tasks_denpendency_row_sum[i] == 0 and tasks_denpendency_col_sum[i] == 0:
#         double_sum += 1
# for i in range(len(end_node_1)):
#     for j in range(len(tasks)):
#         if tasks_dependency[end_node_1[i]][j] == 1:
#             print(False)
# print("start_num", col_sum)
# print("end_num", row_sum)
# print("start_end_num", double_sum)


# start_node = []
# end_node = []
# for i in range(len(pre_task)):
#     if pre_task[i] == []:
#         start_node.append(i)
# a = 0
# for i in range(len(tasks)):
#     for j in range(len(pre_task)):
#         if i in pre_task[j]:
#             a = 1
#             break
#     if a == 0:
#         end_node.append(i)
# print("start_num", len(start_node))
# print("end_num", len(end_node))


