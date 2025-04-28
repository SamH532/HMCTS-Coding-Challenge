import tkinter as tk
import psycopg2
from tkinter import ttk
from enum import Enum
from tkcalendar import DateEntry 


class Interaction(Enum):
    add = 1
    update = 2
    view = 3
    delete = 4

class Status(Enum):
    unstarted = "Unstarted"
    inProgress = "In Progress"
    complete = "Complete"

class Task:

    def __init__(self, taskId, taskTitle, taskDescription, taskStatus, taskDeadline):
        self.taskId = taskId
        self.taskTitle = taskTitle
        self.taskDescription = taskDescription
        self.taskStatus = taskStatus
        self.taskDeadline = taskDeadline

def getTask(idNum) -> Task:
    cursor.execute("SELECT tasktitle, taskdescription, taskstatus, taskdeadline FROM taskstable WHERE taskid = {0};".format(idNum))
    readTask = cursor.fetchone()
    return Task(idNum, readTask[0], readTask[1], Status(readTask[2]), readTask[3])

def taskInDatabase(idNum):
    cursor.execute("""SELECT COUNT(1) FROM taskstable WHERE taskid = {0};""".format(idNum))
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

def getNextTaskId():
    cursor.execute("SELECT MAX(taskid) FROM taskstable")
    try:
        return int(cursor.fetchone()[0]) + 1
    except:
        return 1

def popup(message):
    global popupWindow
    try:
        popupWindow.destroy()
    except:
        pass
    popupWindow = tk.Tk()

    popupWindow.wm_title("Alert")
    label= ttk.Label(popupWindow, text= message, justify= 'left')
    label.pack(side='top', fill='x')
    B1= ttk.Button(popupWindow, text='Okay', command= popupWindow.destroy)
    B1.pack()
    popupWindow.mainloop()

class MainClass(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'Task Manager Program')

        titleLabel = tk.Label(self, text = "Task Manager", anchor=tk.CENTER)
        titleLabel.grid(row=0, column=0, columnspan=6,sticky='ew')

        createTaskButton = tk.Button(self, text="New Task",command= lambda: EditTaskWindow(Interaction.add))
        viewAllTaskButton = tk.Button(self, text="View all tasks", command= lambda: ViewAllWindow())

        createTaskButton.grid(row=1,column=0, sticky='ew',columnspan=3)
        viewAllTaskButton.grid(row=1,column=3, sticky='ew',columnspan=3)

        idLabel = tk.Label(self, text="Task ID:")
        idLabel.grid(row=2,column=0, columnspan=2, sticky='ew')
        self.inputId = ''
        idEntryBox = tk.Entry(self, textvariable = self.inputId)
        idEntryBox.grid(row=2,column=2,columnspan=4,sticky='ew')

        def openExistingTask(interaction, idNum):
            if idNum == '':
                popup("Please enter a task")
            elif taskInDatabase(idNum):
                if interaction is Interaction.view:
                    ViewTaskWindow(Interaction.view, idNum)
                elif interaction is Interaction.update:
                    EditTaskWindow(Interaction.update, idNum)
                elif interaction is Interaction.delete:
                    ViewTaskWindow(Interaction.delete, idNum)
            else:
                popup("Task not found")
            

        viewTaskButton = tk.Button(self, text="View Task", command= lambda: openExistingTask(Interaction.view, idEntryBox.get()))
        updateTaskButton = tk.Button(self, text="Update Task", command= lambda: openExistingTask(Interaction.update, idEntryBox.get()))
        deleteTaskButton = tk.Button(self, text="Delete Task", command= lambda: openExistingTask(Interaction.delete, idEntryBox.get()))
        viewTaskButton.grid(row=3,column=0,columnspan=2,sticky='ew')
        updateTaskButton.grid(row=3,column=2,columnspan=2,sticky='ew')
        deleteTaskButton.grid(row=3,column=4,columnspan=2,sticky='ew')

        self.resizable(width= False, height= False)

        self.mainloop()

class EditTaskWindow(tk.Tk):

    def __init__(self, mode, *inputId):
        
        tk.Tk.__init__(self)
        if mode is Interaction.update:
            tk.Tk.wm_title(self, 'Update Task')
            inputTask = getTask(inputId[0])
            taskId = inputTask.taskId[0]
            taskTitle = inputTask.taskTitle
            taskDescription = inputTask.taskDescription
            taskStatus = inputTask.taskStatus
            taskDeadline = inputTask.taskDeadline
        elif mode is Interaction.add:
            tk.Tk.wm_title(self, 'Add Task')
            taskId = getNextTaskId()
            taskTitle = ""
            taskDescription = ""
            taskStatus = Status.unstarted
            taskDeadline = ""
        else:
            exit

        titleLabel = tk.Label(self, text= "Title:", anchor=tk.W)
        titleLabel.grid(column=0, row=1, sticky='ew')
        titleEntry = tk.Entry(self, textvariable = taskTitle)
        titleEntry.insert(0, taskTitle)
        titleEntry.grid(column=1,row=1, sticky='ew')

        
        descriptionLabel = tk.Label(self, text= "Description:", anchor=tk.W)
        descriptionLabel.grid(column=0, row=2, sticky='ew')
        descriptionEntry = tk.Text(self)
        descriptionEntry.insert('1.0', taskDescription)
        descriptionEntry.grid(column=1,row=2, sticky='ew')

        
        statusLabel = tk.Label(self, text= "Status:", anchor=tk.W)
        statusLabel.grid(column=0, row=3, sticky='ew')
        statusEntry = tk.Listbox(self,exportselection=False)
        counter = 0
        statusEntryList = []
        for stat in Status:
            statusEntryList.append(stat.value)
            statusEntry.insert(counter,stat.value)
            if mode is Interaction.update and taskStatus.value is stat.value:
                statusEntry.select_set(counter)
            counter += 1

        if mode is Interaction.add:
            statusEntry.select_set(0)
    
        statusEntry.config(height= statusEntry.size())
        statusEntry.grid(column=1,row=3, sticky='ew')

        def getStatus():
            return Status(statusEntry.get(statusEntry.curselection()))

        
        deadlineLabel = tk.Label(self, text= "Deadline:", anchor=tk.W)
        deadlineLabel.grid(column=0, row=4, sticky='ew')
        deadlineEntry = DateEntry(self, textvariable = taskDeadline, date_pattern="yyyy-mm-dd")
        deadlineEntry.delete(0,"end")
        deadlineEntry.insert(0, taskDeadline)
        deadlineEntry.grid(column=1,row=4, sticky='ew')

        if mode is Interaction.update:
            submitButton = tk.Button(self, text="Update Task", command = lambda: updateTask(taskId, titleEntry.get(), descriptionEntry.get('1.0', 'end'), getStatus(), deadlineEntry.get()))
        elif mode is Interaction.add:
            submitButton = tk.Button(self, text="Create Task", command = lambda: createTask(taskId, titleEntry.get(), descriptionEntry.get('1.0', 'end'), getStatus(), deadlineEntry.get()))
        submitButton.grid(column=0,row=5,columnspan=2)

        def createTask(taskId, taskTitle, taskDescription, taskStatus, taskDeadline):
            pass
            if validateEntries(taskTitle, taskStatus, taskDeadline):
                cursor.execute("""
                                INSERT INTO taskstable (taskid, tasktitle, taskdescription, taskstatus, taskdeadline) VALUES ({0}, '{1}', '{2}', '{3}', '{4}');
                                """.format(taskId, taskTitle, taskDescription, taskStatus.value, taskDeadline)
                               )
                conn.commit()
                self.destroy()
            else:
                pass
        def updateTask(taskId, taskTitle, taskDescription, taskStatus, taskDeadline):
            if validateEntries(taskTitle, taskStatus, taskDeadline):
                cursor.execute("""
                                UPDATE taskstable
                                SET tasktitle = '{1}', taskdescription = '{2}', taskstatus = '{3}', taskdeadline = '{4}'
                                WHERE taskid = {0};
                                """.format(taskId, taskTitle, taskDescription, taskStatus.value, taskDeadline)
                               )
                conn.commit()
                self.destroy()
            else:
                pass

        def validateEntries(taskTitle, taskStatus, taskDeadline):

            boolList = []
            failList = []

            if taskTitle != '':
                boolList.append(True)
            else:
                boolList.append(False)
                failList.append("Title")

            if taskStatus in Status:
                boolList.append(True)
            else:
                boolList.append(False)
                failList.append("Status")

            if taskDeadline != '' and len(taskDeadline) <= 16:
                boolList.append(True)
            else:
                boolList.append(False)
                failList.append("Deadline")
            
            if boolList.count(False) == 0:
                return True
            else:
                popup("The following entries are invalid: \n - " +'\n - '.join(failList))
                return False

        self.mainloop()

class ViewTaskWindow(tk.Tk):
    def __init__(self, mode, inputId):
        tk.Tk.__init__(self)
        inputTask = getTask(inputId)
        taskId = inputTask.taskId
        taskTitle = inputTask.taskTitle
        taskDescription = inputTask.taskDescription
        taskStatus = inputTask.taskStatus
        taskDeadline = inputTask.taskDeadline
        if mode is Interaction.view:
            tk.Tk.wm_title(self, 'View Task')
        elif mode is Interaction.delete:
            tk.Tk.wm_title(self, 'Delete Task')

        idLabel = tk.Label(self, text="ID:", anchor=tk.W)
        idLabel.grid(column=0,row=0, sticky='w')
        idEntry = tk.Entry(self, textvariable = taskId)
        idEntry.insert(0, taskId)
        idEntry.config(state='disabled')
        idEntry.grid(column=1,row=0,sticky='e')

        titleLabel = tk.Label(self, text= "Title:", anchor=tk.W)
        titleLabel.grid(column=0, row=1, sticky='w')
        titleEntry = tk.Entry(self, textvariable = taskTitle)
        titleEntry.insert(0, taskTitle)
        titleEntry.config(state='disabled')
        titleEntry.grid(column=1,row=1, sticky='e')

        
        descriptionLabel = tk.Label(self, text= "Description:", anchor=tk.W)
        descriptionLabel.grid(column=0, row=2, sticky='w')
        descriptionEntry = tk.Entry(self, textvariable = taskDescription)
        descriptionEntry.insert(0, taskDescription)
        descriptionEntry.config(state='disabled')
        descriptionEntry.grid(column=1,row=2, sticky='e')
        
        statusLabel = tk.Label(self, text= "Status:", anchor=tk.W)
        statusLabel.grid(column=0, row=3, sticky='w')
        statusEntry = tk.Entry(self, textvariable = taskStatus)
        statusEntry.insert(0, taskStatus.value)
        statusEntry.config(state='disabled')
        statusEntry.grid(column=1,row=3, sticky='e')
        
        deadlineLabel = tk.Label(self, text= "Deadline:", anchor=tk.W)
        deadlineLabel.grid(column=0, row=4, sticky='w')
        deadlineEntry = tk.Entry(self, textvariable = taskDeadline)
        deadlineEntry.insert(0, taskDeadline)
        deadlineEntry.config(state='disabled')
        deadlineEntry.grid(column=1,row=4, sticky='e')

        if mode is Interaction.delete:
            deleteButton = tk.Button(self, text="Confirm Delete?", command = lambda: deleteTask(taskId))
            deleteButton.grid(column=0, columnspan=2, row=5)

        def deleteTask(taskId):
            cursor.execute("DELETE FROM taskstable WHERE taskid = {0}".format(taskId))
            conn.commit()
            self.destroy()

        self.mainloop()

class ViewAllWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'View All Tasks')
        rowNum = 1
        tree = ttk.Treeview(self, columns=['Title', 'Deadline'])

        def getAllTasks(): 
            cursor.execute("SELECT taskid, tasktitle, taskdescription, taskstatus, taskdeadline FROM taskstable")
            taskList = []
            for item in cursor.fetchall():
                taskList.append(Task(item[0], item[1], item[2], Status(item[3]), item[4]))
            return taskList

        for task in getAllTasks():
            tree.insert('', tk.END, text=task.taskId, values=[task.taskTitle, task.taskDeadline])

        tree.heading("#0", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Deadline", text="Deadline")

        tree.pack(fill=tk.BOTH)

        self.resizable(width= False, height= False)

        self.mainloop()


global conn
conn = psycopg2.connect(database="taskdb",
                        host='127.0.0.1',
                        user='postgres',
                        port=5432)
global cursor
cursor = conn.cursor()

MainClass()
