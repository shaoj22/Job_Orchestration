'''
File: draw_utils.py
Project: Job Orchestration
Description:
-----------
utils for the job orchestration, such as plt tools
-----------
Author: 626
Created Date: 2023-0719
'''
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 
class draw_utils():
    def draw_resource_line_chart(self, data):
        """
        绘制调度结果资源的折线图
        input the solution of start time and the infomation of tasks
        ouput the resource load of each-time
        """
        # 创建子图
        fig, ax = plt.subplots(figsize=(12, 6))
        # 生成x轴刻度标签
        x_labels = range(len(data))
        # 减少数据点的显示数量，使用每隔一定间隔的数据点
        interval = max(len(data) // 20, 1)
        x_labels_sampled = x_labels[::interval]
        data_sampled = data[::interval]
        # 绘制折线图，使用平滑的线条
        x_smooth = np.linspace(min(x_labels), max(x_labels), 300)
        data_smooth = np.interp(x_smooth, x_labels, data)
        ax.plot(x_smooth, data_smooth, color='b', linewidth=2, label='Resource Load')
        # 设置图形标题和轴标签
        ax.set_title('Line Chart - Resource Load')
        ax.set_xlabel('Time')
        ax.set_ylabel('Resource Load')
        ax.set_ylim(0, 1)
        # 设置x轴刻度标签
        ax.set_xticks(x_labels_sampled)
        ax.set_xticklabels(x_labels_sampled)
        # 设置y轴刻度标签
        y_labels = [i/5 for i in range(6)]
        ax.set_yticks(y_labels)
        ax.set_yticklabels(y_labels)
        # 添加网格线
        ax.grid(True, which='both', linestyle='--', linewidth = 0.5)
        # 添加图例
        ax.legend()
        # 显示图形
        plt.tight_layout()
        plt.show()

    def draw_parallelism_line_chart(self, data):
        """
        绘制调度结果并行任务的折线图
        输入每个时刻正在执行的任务数量数据
        """
        # 生成x轴刻度标签
        x_labels = range(len(data))
        # 减少数据点的显示数量，使用每隔一定间隔的数据点
        interval = max(len(data) // 20, 1)
        x_labels_sampled = x_labels[::interval]
        data_sampled = data[::interval]
        # 绘制折线图，使用平滑的线条
        x_smooth = np.linspace(min(x_labels), max(x_labels), 300)
        data_smooth = np.interp(x_smooth, x_labels, data)
        
        # 创建图形并设置美化参数
        plt.figure(figsize=(12, 6))
        plt.plot(x_smooth, data_smooth, color='r', linewidth=2, label='Job Parallelism')
        # 设置图形标题和轴标签
        plt.title('Line Chart - Job Parallelism')
        plt.xlabel('Time')
        plt.ylabel('Job Parallelism')
        plt.ylim(0, 100)  # 将y轴上限设置为任务数量的最大值加上一些空间
        # 设置x轴刻度标签
        plt.xticks(x_labels_sampled)  # 旋转x轴刻度标签，以避免重叠
        # 添加网格线
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        # 添加图例
        plt.legend()
        # 显示图形
        plt.tight_layout()  # 调整布局，以确保图形各元素不重叠
        plt.show()

    def draw_gantt_chart(self, start_times, durations, task_names):
        """
        绘制调度结果的甘特图
        输入任务的开始时间、持续时间和任务名称
        输出各时间点的资源负载
        """
        # 确定任务数量
        num_tasks = len(start_times)
        # 设置图形大小
        fig_height = min(num_tasks * 0.3, 10)
        fig, ax = plt.subplots(figsize=(10, fig_height))
        # 设置y轴刻度标签和任务名称（折叠显示）
        step = max(1, num_tasks // 50)  # 控制每隔多少任务显示一个名称
        visible_task_names = task_names[::step]
        visible_ticks = np.arange(0, num_tasks, step)
        ax.set_yticks(visible_ticks)
        ax.set_yticklabels(visible_task_names, fontsize=12)
        # 确定时间范围，限制显示前200个时间步
        max_time = min(max(start_times) + max(durations), 1440)
        ax.set_xlim(0, max_time)
        # 使用viridis颜色映射
        cmap = plt.get_cmap('viridis', num_tasks)
        # 遍历每个任务
        for i in range(num_tasks):
            start_time = start_times[i]
            duration = durations[i]
            end_time = start_time + duration
            # 限制在时间范围内绘制甘特图线段
            if start_time < max_time:
                y_val = i
                ax.hlines(y=y_val, xmin=start_time, xmax=min(end_time, max_time), colors=cmap(i), linewidth=3)
        # 设置图形标题和轴标签
        ax.set_title('gantt chart', fontsize=18, fontweight='bold')
        ax.set_xlabel('time', fontsize=14)
        ax.set_ylabel('task', fontsize=14)
        # 隐藏y轴刻度线
        ax.yaxis.set_ticks_position('none')
        # 移除上方和右侧的边框
        sns.despine(top=True, right=True)
        # 添加网格线
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        # 设置背景颜色
        plt.gca().set_facecolor('#f0f0f0')
        # 显示图形
        plt.tight_layout()
        plt.show()