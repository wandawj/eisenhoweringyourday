import pandas as pd
from pulp import *
import numpy as np

def eisenhower(task_file_name, schedule_file_name):
    tasks = pd.read_csv(task_file_name)
    tasks

    schedule = pd.read_csv(schedule_file_name)['Availability']
    schedule

    s = list(tasks['Important score (1-5)'])
    d = list(tasks['Num of blocks'])
    b = list(schedule)

    B = len(b)
    n = len(s)

    # time blocks available

    A = sum(b)


    prob = LpProblem("Schedule_Tasks", LpMaximize)

    y = LpVariable.dicts('Block', [(i,t) for i in range(n) for t in range(B)], cat='Binary')

    prob += lpSum(s[i]*b[t]*y[(i,t)] for i in range(n) for t in range(B))


    prob += lpSum(y[(i,t)] for i in range(n) for t in range(B)) <= A #1

    for i in range(n):
        prob += lpSum(y[(i,t)] for t in range(B)) <= d[i] #2

    for t in range(B):
        prob += lpSum(y[(i,t)] for i in range(n)) <= 1 #3

    prob.solve()

    tasks = np.zeros((n,B))
    chosen_tasks = []
    print("Assignment accomplished!")
    for i in range(n):
        for t in range(B):
            tasks[i][t]= y[(i,t)].varValue*(i+1)
            if y[(i,t)].varValue == 1:
                if i+1 not in chosen_tasks:
                    chosen_tasks.append(i+1)

    print('Chosen tasks are: {}'.format(chosen_tasks))

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize = (20,20))
    #1x1 grid, first subplot
    ax = fig.add_subplot(111)
    #Make the y-axis invisible
    ax.axes.get_yaxis().set_visible(False)
    #Set the ratio of y-unit to x-unit
    ax.set_aspect(1)

    def avg(a, b):
        return (a + b) / 2.0

    #y is the order of row, row is the data of the rows
    for y, row in enumerate(tasks):
        for x, col in enumerate(row):
            x1 = [x, x+1]
            y1 = [0, 0]
            y2 = [3, 3]

            if col == 1:
                #Fill the area between two horizontal curves.
                plt.fill_between(x1, y1, y2=y2, color='red')
                #Fill the text in the middle of 2 units in x and y-axis
                plt.text(avg(x1[0], x1[1]), avg(y1[0],y2[0]), "0",
                        horizontalalignment='center', verticalalignment='center')

            if col == 2 :
                #Fill the area between two horizontal curves.
                plt.fill_between(x1, y1, y2=y2, color='pink')
                #Fill the text in the middle of 2 units in x and y-axis
                plt.text(avg(x1[0], x1[1]), avg(y1[0],y2[0]), "1",
                        horizontalalignment='center', verticalalignment='center')

            if col == 4:
                #Fill the area between two horizontal curves.
                plt.fill_between(x1, y1, y2=y2, color='green')
                #Fill the text in the middle of 2 units in x and y-axis
                plt.text(avg(x1[0], x1[1]), avg(y1[0],y2[0]), "3",
                        horizontalalignment='center', verticalalignment='center')

            if col == 5:
                #Fill the area between two horizontal curves.
                plt.fill_between(x1, y1, y2=y2, color='purple')
                #Fill the text in the middle of 2 units in x and y-axis
                plt.text(avg(x1[0], x1[1]), avg(y1[0],y2[0]), "4",
                        horizontalalignment='center', verticalalignment='center')

            if col == 7:
                #Fill the area between two horizontal curves.
                plt.fill_between(x1, y1, y2=y2, color='blue')
                #Fill the text in the middle of 2 units in x and y-axis
                plt.text(avg(x1[0], x1[1]), avg(y1[0],y2[0]), "6",
                        horizontalalignment='center', verticalalignment='center')

    ax.set_xlabel('Block Number')
    plt.savefig('eisenhowerblock.png')