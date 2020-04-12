# -*- coding: utf-8 -*-
# @Time : 2020-04-11
# @Author : HXY
# @File : task.py

import pymysql
import os
from matplotlib import pyplot as plt


class NonCriticalWork:
    """
    非关键性工作
    """
    # 非关键工作名称
    work_name = ''
    # 任务名称
    task_name = ''
    # 最早开始是时间
    oldest_begin_time = 0
    # 最早完成时间
    oldest_complete_time = 0
    # 资源量
    resource = 0
    # 资源动态图
    resource_dynamic_graph = {}
    # 推迟天数
    delay_days = 0
    # 每天的资源量
    day_resource = 0
    # 自由时差
    free_time_difference = 0


class Task:
    """
    施工任务
    """
    # 任务名称
    task_name = ''
    # 最早开始是时间
    oldest_begin_time = 0
    # 最早完成时间
    oldest_complete_time = 0
    # 资源量
    resource = 0
    # 资源动态图
    resource_dynamic_graph = {}
    # 非关键性工作集合
    critical_work_list = []
    # 非关键性工作集合
    non_critical_work_list = []


def init_task():
    """
    初始化任务
    """
    # 链接数据库
    db = pymysql.connect(host="localhost", user="root",
                         password="HXY950504", db="honeybee", charset="utf8")
    cursor = db.cursor()

    task_list = []

    # 查询数据库，填充任务,
    query_task_sql = "SELECT * FROM TASK"
    cursor.execute(query_task_sql)
    query_task_list = cursor.fetchall()
    for query_task in query_task_list:
        if query_task is not None:
            task = Task()
            task.task_name = query_task[0]
            task.oldest_begin_time = query_task[1]
            task.oldest_complete_time = query_task[2]
            task.resource = query_task[3]

            # 根据任务ID查询非关键工作,并且按照最早开始时间排序
            query_non_critical_work_sql = "SELECT * FROM CRITICAL_WORK WHERE IS_CRITICAL_WORK = 0 AND TASK_NAME = " + \
                "\"" + task.task_name + "\"" + " ORDER BY OLDEST_BEGIN_TIME DESC"
            cursor.execute(query_non_critical_work_sql)
            query_non_critical_work_result = cursor.fetchall()
            task.non_critical_work_list = complete_work(query_non_critical_work_result)

            # 根据任务ID查询关键工作,并且按照最早开始时间排序
            query_critical_work_sql = "SELECT * FROM CRITICAL_WORK WHERE IS_CRITICAL_WORK = 1 AND TASK_NAME = " + \
                "\"" + task.task_name + "\"" + " ORDER BY OLDEST_BEGIN_TIME DESC"
            cursor.execute(query_critical_work_sql)
            query_critical_work_result = cursor.fetchall()
            task.critical_work_list = complete_work(query_critical_work_result)

            init_task_resource_dynamic_graph(task)
            task_list.append(task)

    db.close()
    return task_list


def complete_work(query_result):
    """
    将数据库结果转化成任务对象
    """
    query_work_list = []
    for query_work in query_result:
        if query_work is not None:
            critical_work = NonCriticalWork()
            critical_work.work_name = query_work[0]
            critical_work.task_name = query_work[1]
            critical_work.oldest_begin_time = query_work[2]
            critical_work.oldest_complete_time = query_work[3]
            critical_work.resource = query_work[4]
            critical_work.free_time_difference = query_work[5]
            critical_work.day_resource = query_work[4] / (
                query_work[3] - query_work[2] + 1)
            init_work_resource_dynamic_graph(critical_work)
            query_work_list.append(critical_work)
    return query_work_list


def init_work_resource_dynamic_graph(work):
    """
    初始化每一个工作的资源动态图
    """
    resource_dynamic_graph = {}
    all_days = work.oldest_complete_time - work.oldest_begin_time + 1
    day_resource = work.resource / all_days
    for day in range(1, all_days + 1):
        resource_dynamic_graph[day] = day_resource
    work.resource_dynamic_graph = resource_dynamic_graph


def init_task_resource_dynamic_graph(task):
    """
    初始化任务的资源动态图
    """
    resource_dynamic_graph = {}
    critical_work_list_reverse = task.critical_work_list
    critical_work_list_reverse.reverse()
    resource_dynamic_graph = critical_work_list_reverse[0].resource_dynamic_graph
    begin_day = len(resource_dynamic_graph)
    for critical_work in critical_work_list_reverse[1:]:
        for resource in critical_work.resource_dynamic_graph.values():
            resource_dynamic_graph[begin_day + 1] = resource
            begin_day += 1

    non_critical_work_list_reverse = task.non_critical_work_list
    non_critical_work_list_reverse.reverse()
    for non_critical_work in non_critical_work_list_reverse:
        oldest_begin_time = non_critical_work.oldest_begin_time
        oldest_complete_time = non_critical_work.oldest_complete_time
        for day in range(oldest_begin_time, oldest_complete_time + 1):
            resource_dynamic_graph[day] = resource_dynamic_graph[day] + \
                non_critical_work.day_resource

    task.resource_dynamic_graph = resource_dynamic_graph


def adjust_task(task_list):
    """
    调整任务
    """
    # 遍历任务列表，取出每一个任务
    for task in task_list:
        # 遍历每一个任务，取出他的每一个非关键性任务，从最后一个非惯性任务开始
        non_critical_work_list = task.non_critical_work_list
        non_critical_work_list.reverse()
        free_time = 0
        for non_critical_work in non_critical_work_list:
            non_critical_work.free_time_difference += free_time
            # 根据自由时差一步一步调整任务的最晚开始是时间，在判段公式13,调整一天，说明推迟一天，推迟天数加1，最晚开始时间-1
            time = 1
            while time <= non_critical_work.free_time_difference:
                non_critical_work.oldest_begin_time = non_critical_work.oldest_begin_time + 1
                non_critical_work.oldest_complete_time = non_critical_work.oldest_complete_time + 1
                non_critical_work.delay_days += 1
                # 如果满足公式13，则说明不存在可调整的余地，不调整这个工作，退出当前这个循环，然后拿到下一个任务进行调整
                if not expression13(non_critical_work, task):
                    non_critical_work.delay_days -= 1
                    break
                # 否则说明该任务可调整，调用调整的算法进行调整
                else:
                    adjust_resource_again(non_critical_work, task)
                time += 1
            free_time = non_critical_work.delay_days
            write_result("非关键工作[" + non_critical_work.work_name +
                         "]延迟天数：" + str(non_critical_work.delay_days))
        print(task.resource_dynamic_graph)


def expression13(non_critical_work, task):
    """
    公式13
    """
    task_resource_dynamic_graph = task.resource_dynamic_graph

    complete_time = non_critical_work.oldest_complete_time
    begin_time = non_critical_work.oldest_begin_time - 1
    # param1
    complete_time_resource = task_resource_dynamic_graph[complete_time]
    # param2
    being_time_resource = task_resource_dynamic_graph[begin_time]
    # param3
    day_resource = non_critical_work.day_resource

    is_move_before = True if complete_time_resource - \
        being_time_resource + day_resource < 0 else False
    is_no_free_time_difference = True if non_critical_work.delay_days - \
        non_critical_work.free_time_difference <= 0 else False

    if is_no_free_time_difference and is_move_before:
        return True
    else:
        return False


def adjust_resource_again(non_critical_work, task):
    """
    重新在调整资源
    """
    task_resource_dynamic_graph = task.resource_dynamic_graph
    oldest_begin_time = non_critical_work.oldest_begin_time
    oldest_complete_time = non_critical_work.oldest_complete_time

    # 由于推迟了一天，所以任务中对应开始的那天资源要做减法
    task_resource_dynamic_graph[oldest_begin_time - 1] = task_resource_dynamic_graph[oldest_begin_time - 1] - \
        non_critical_work.day_resource

    # 推迟的那天开始每天要做加法
    for day in range(oldest_begin_time + 1, oldest_complete_time + 1):
        task_resource_dynamic_graph[day] = task_resource_dynamic_graph[day] + \
            non_critical_work.day_resource


def draw_plt(task):
    """
    画资源分布图
    """
    resource_dynamic_graph = task.resource_dynamic_graph
    keys = resource_dynamic_graph.keys()
    values = []
    for value in resource_dynamic_graph.values():
        values.append(value)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(range(1, len(keys) + 1), values)
    plt.title('资源分布图')
    plt.xlabel('D')
    plt.ylabel('R')
    plt.savefig('资源分布图.png')
    plt.show()


def write_result(content):
    """
    写入文件
    """
    with open('result.txt', 'a', encoding='utf-8') as file:
        file.write(content)
        file.write(('\n'))


if __name__ == "__main__":
    task_list = init_task()
    adjust_task(task_list)
    draw_plt(task_list[0])
