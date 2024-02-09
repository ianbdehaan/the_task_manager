import os, sys, getopt
import pandas as pd

class Tasks:
    tasks = pd.read_csv('tasks.csv')
    def to_markdown(self):
        ''' TODO transform the csv file with the tasks into a markdown file '''
        pass
    def new_task(self, name, start, end, reminder):
        ''' TODO add a new task to the csv file '''
        tasks.append({'Name' = name, 'Start' = start, 'End' = end, 'Reminder' = reminder}, ignore_index = True)
    def mark(self, name):
        ''' TODO mark a certain task as completed '''
        pass
    def list(self, complete = False):
        ''' Todo list the tasks '''
        pass
    def __repr__(self): 
        ''' TODO a printable representation of the tasks'''
        display(tasks)
    def delete(name):
        ''' TODO delete a particular task '''
        pass

def main():
    if not os.path.isfile('tasks.csv'):
        f = open('tasks.csv', w)
        f.write('Name,Start,End,Reminder,Status')
        f.close()
    tasks_instance = Tasks()
    optlist, args = getopt.getopt(sys.argv[1:])
    match optlist[0][0]:
        case '-d':
            tasks_instance.delete(optlist[0][1])
        case '-m':
            tasks_instance.mark(optlist[0][1])
        case '-c'
            tasks_instance.create(optlist[0][1], arg)

