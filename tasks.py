import os
import sys
import csv
import re
import datetime as dt
from tabulate import tabulate


class Tasks:
    def __init__(self):
        self.tasks = []
        with open('tasks.csv', 'r') as task_file:
            reader = csv.reader(task_file)        
            for line in reader:
                self.tasks.append(line)

    def to_markdown(self):
        ''' TODO transform the csv file with the tasks into a markdown file '''
        pass

    def new_task(self, name, received_dates):
        '''  add a new task to the csv file '''
        # the idea is that the person doesn't have to pass any date, and month and year will be infered as the current year
        # if nothing else is passed TODO: infer year as next year or month as next month if day/ month are already in the future
        dates = [None]*3
        for i in range(len(received_dates)):
            match len(received_dates[i].split('-')):
                case 1:
                    today = dt.date.today()
                    if today.day <= int(received_dates[i]):
                        dates[i] = '{:02d}-{:02d}-{:4d}'.format(int(received_dates[i]), today.month, today.year)
                    elif today.month == 12:
                        dates[i] = '{:02d}-{:02d}-{:4d}'.format(int(received_dates[i]), 1, today.year)
                    else:
                        dates[i] = '{:02d}-{:02d}-{:4d}'.format(int(received_dates[i]), today.month + 1, today.year)
                case 2:
                    today = dt.date.today()
                    task_day, task_month = int(received_dates[i].split('-')) 
                    if (today.month > task_month):
                        dates[i] = '{:02d}-{:02d}-{:4d}'.format(int(task_day), int(task_month), today.year + 1)
                    else:
                        dates[i] = '{:02d}-{:02d}-{:4d}'.format(int(task_day), int(task_month), today.year)
                case 3:
                    task_date = received_dates[i].split('-')
                    dates[i] = '{:02d}-{:02d}-{:4d}'.format(int(task_date[0]), int(task_date[1]), task_date[2])
        self.tasks.append([name, dates[0], dates[1], dates[2], None, None])

    def mark(self, name):
        ''' TODO mark a certain task as completed '''
        for task in self.tasks:
            if re.match(name,task[0]):
                today = dt.date.today()
                task[4] = 'x'
                task[5] = '{:02d}-{:02d}-{:4d}'.format(today.day,today.month,today.year)

    def list(self, complete=False):
        ''' Todo list the tasks '''
        pass

    def display(self, option = 'simple', sort_by = 1):
        '''display the tasks in usefull ways'''
        def key_function(date):
            if not date[sort_by]:
                return '999999999'
            else:
                 return ''.join(date[sort_by].split('-')[::-1])
        match option:
            case 'all':
                '''display in the chosen sorting ignoring if tasks are marked or not'''
                return tabulate(sorted(self.tasks[1:],key = key_function),
                                headers = self.tasks[0])
            case 'ordered':
                '''marked tasks appear last'''
                sorted_not_done = sorted([task for task in self.tasks[1:] if task[4] != 'x'], 
                                         key = key_function)
                sorted_marked = sorted([task for task in self.tasks[1:] if task[4] == 'x'], 
                                       key = key_function)
                return tabulate(sorted_not_done+sorted_marked, headers=self.tasks[0])
            case 'simple':
                '''intended to be used for simple viewing of the tasks to be done,
                marked tasks and columns related to marking are not shown'''
                sorted_not_done = sorted([task[:4] for task in self.tasks[1:] if task[4] != 'x'], 
                                         key = key_function)
                return tabulate(sorted_not_done, headers=self.tasks[0])
            case 'marked':
                '''intended to be used to visualize the marked tasks only marked tasks are shown'''
                sorted_marked = sorted([task for task in self.tasks[1:] if task[4] == 'x'], 
                                       key = key_function)
                return tabulate(sorted_marked, headers=self.tasks[0])
            case '-h':
                return 'The available options are: all, ordered, simple, marked'
            case _:
                '''person inserted a wrong command for viewing'''
                raise Exception('''You are using view with an unavailable option\n
                                The available options are: all, ordered, simple, marked''')

    def __repr__(self):
        '''  a printable representation of the tasks'''
        return tabulate(self.tasks, headers = "firstrow")

    def delete(self, name):
        ''' delete a particular task, not through regex because its risky'''
        for task in self.tasks:
            if task[0] == name:
                self.tasks.remove(task)

    def save(self):
        '''saves the tasks as a csv file'''
        with open('tasks.csv', 'w', newline = '') as task_file:
            writer = csv.writer(task_file)
            for task in self.tasks:
                writer.writerow(task)

def process_cl_args():
    match len(sys.argv):
        case 1:
            command = '-h'
            args = []
            return command, args
        case 2:
            command = sys.argv[1]
            args = []
            return command, args
        case _:
            command = sys.argv[1]
            args = sys.argv[2:]
            return command, args

def process_command(command, args):

    tasks_instance = Tasks()
    match command:
        case 'del':
            '''deleting a task'''
            tasks_instance.delete(args[0])
            print(tasks_instance.display(option='all'))
        case 'mark':
            '''marking a task'''
            tasks_instance.mark(args[0])
            print(tasks_instance.display(option='only',sort_by=5))
        case 'add':
            '''create a task'''
            tasks_instance.new_task(args[0], args[1:])
            print(tasks_instance.display())
        case 'list':
            '''visualizing the tasks'''
            if len(args)==2:
                sorting_options = {'name':0, 'start': 1, 'end': 2, 'reminder':3,
                                    'status':4, 'completed_in':5, 'completed': 5}
                print(tasks_instance.display(option=args[0], sort_by=sorting_options[args[1]]))
            elif len(args)==1:
                print(tasks_instance.display(option=args[0]))
            else:
                print(tasks_instance.display())
        case '-h':
            print(
'''
usage: tasks.py [command] *args, where *args depend on the chosen command

Available commands:
add [start] [optional: end] [optional: reminder_date]
dates should be either in ther format dd-mm-yyyy, dd-mm with year infered, or dd with mm-yyyy infered

mark [regex]
marks any tasks whose names match the regex

del [name]
delete any tasks with the specified name

list [optional:option] [optional:sort_by]
options are: [all, ordered, simple, marked]
sort_by can be any column in the tasks file''')
    tasks_instance.save()
    
             
def main():

    if not os.path.isfile('tasks.csv'):
        f = open('tasks.csv', "w")
        f.write('name,start,end,reminder,status,completed_in')
        f.close()
    command, args = process_cl_args()
    process_command(command, args)

main()
