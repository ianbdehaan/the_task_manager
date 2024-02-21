import os
import sys
import getopt
import csv
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
                        dates[i] = '{:2s}-{:02d}-{:4d}'.format(received_dates[i], today.month, today.year)
                    elif today.month == 12:
                        dates[i] = '{:2s}-{:02d}-{:4d}'.format(received_dates[i], 1, today.year)
                    else:
                        dates[i] = '{:2s}-{:02d}-{:4d}'.format(received_dates[i], today.month + 1, today.year)
                case 2:
                    today = dt.date.today()
                    if today.month > int(received_dates[i].split('-')[1]):
                        dates[i] = f"{received_dates[i]}-{today.year+1}"
                    else:
                        dates[i] = f"{received_dates[i]}-{today.year}"
                case 3:
                    dates[i] = received_dates[i]
        self.tasks.append([name, dates[0], dates[1], dates[2], None, None])

    def mark(self, name):
        ''' TODO mark a certain task as completed '''
        for task in self.tasks:
            if task[0] == name:
                today = dt.date.today()
                task[4] = 'x'
                task[5] = '{:02d}-{:02d}-{:4d}'.format(today.day,today.month,today.year)

    def list(self, complete=False):
        ''' Todo list the tasks '''
        pass

    def display(self, done = 'ignore', sort_by = 2):
        '''display the tasks in usefull ways'''
        match done:
            case 'normal':
                '''display in the chosen sorting ignoring if tasks are marked or not'''
                return tabulate(sorted(self.tasks[1:], 
                                key = lambda date: ''.join(date[sort_by].split('-')[::-1])),
                                 headers = self.tasks[0])
            case 'last':
                '''marked tasks appear last'''
                sorted_not_done = sorted([task for task in self.tasks[1:] if task[4] != 'x'], 
                                         key = lambda date: ''.join(date[sort_by].split('-')[::-1]))
                sorted_marked = sorted([task for task in self.tasks[1:] if task[4] == 'x'], 
                                       key = lambda date: ''.join(date[sort_by].split('-')[::-1]))
                return tabulate(sorted_not_done+sorted_marked, headers=self.tasks[0])
            case 'ignore':
                '''marked tasks are not shown'''
                sorted_not_done = sorted([task for task in self.tasks[1:] if task[4] != 'x'], 
                                         key = lambda date: ''.join(date[sort_by].split('-')[::-1]))
                return tabulate(sorted_not_done, headers=self.tasks[0])
            case 'only':
                '''only marked tasks are shown'''
                sorted_marked = sorted([task for task in self.tasks[1:] if task[4] == 'x'], 
                                       key = lambda date: ''.join(date[sort_by].split('-')[::-1]))
                return tabulate(sorted_marked, headers=self.tasks[0])

    def __repr__(self):
        '''  a printable representation of the tasks'''
        return tabulate(self.tasks, headers = "firstrow")

    def delete(self, name):
        ''' TODO delete a particular task '''
        pass

    def save(self):
        '''saves the tasks as a csv file'''
        with open('tasks.csv', 'w', newline = '') as task_file:
            writer = csv.writer(task_file)
            for task in self.tasks:
                writer.writerow(task)

def main():
    if not os.path.isfile('tasks.csv'):
        f = open('tasks.csv', "w")
        f.write('Name,Start,End,Reminder,Status,Completed_in')
        f.close()
    tasks_instance = Tasks()
    optlist, args = getopt.getopt(sys.argv[1:], 'd:m:c:t:v')

    match optlist[0][0]:
        case '-d':
            '''deleting a task'''
            tasks_instance.delete(optlist[0][1])
            print(tasks_instance.display(done='normal'))
        case '-m':
            '''marking a task'''
            tasks_instance.mark(optlist[0][1])
            print(tasks_instance.display(done='only',sort_by=5))
        case '-t':
            '''create a task'''
            tasks_instance.new_task(optlist[0][1], args)
            print(tasks_instance.display())
        case '-c':
            pass
        case '-v':
            '''visualizing the tasks'''
            print(args)
            if len(args)==2:
                print('hi')
                print(tasks_instance.display(done=args[1], sort_by=int(args[0])))
            elif len(args)==1:
                print(tasks_instance.display(sort_by=int(args[0])))                
            else:
                print(tasks_instance.display())
    tasks_instance.save()


main()
