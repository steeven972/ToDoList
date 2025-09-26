import time
import json 
import os
class Task:
    COUNT = 0
    LIST = {}

    def __init__(self, name=None, data=None, task_id=None):
        if data:  # reconstruction depuis JSON
            self.id = int(task_id)
            self.name = data["name"]
            self.date = data["date"]
            self.status = data["status"]
            
        else:  # création d'une nouvelle tâche
            self.name = name
            self.date = time.strftime("%a %d %b %Y %H:%M:%S", time.localtime())
            self.status = False
            Task.COUNT += 1
            self.id = Task.COUNT
            Task.LIST[Task.COUNT] = []
            Task.LIST[Task.COUNT].append({
                "name": self.name,
                "date": self.date,
                "status": self.status
            })
            Task.save_data(Task.LIST)


    def get_status(self):
        return self.status
    
    def get_time(self):
        return self.date
    
    def set_status(self, index, state):
        self.status = state
        return self.status
    
    @classmethod
    def save_data(cls, data):
        with open("./data/Task.json", "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls):
        with open("./data/Task.json", "r") as f:
            return json.load(f)
            
   
    @classmethod
    def remove_task(cls, task_id):
        task_id = str(task_id)
        data = cls.load()

        if task_id in data:
            # Supprimer la tâche
            del data[task_id]

            new_data = {}
            keys = sorted(map(int, data.keys()))  
            new_id = 1
            for k in keys:
                new_data[str(new_id)] = data[str(k)]
                new_id += 1

            
            cls.LIST = new_data
            cls.COUNT = len(new_data)  # ajuster le compteur
            cls.save_data(new_data)

            print(f"Task {task_id} has been removed and keys reindexed")
        else:
            print("Invalid task ID")






        



