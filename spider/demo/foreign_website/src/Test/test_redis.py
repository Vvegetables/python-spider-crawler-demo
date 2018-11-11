from spider.Task import Task
import redis

class Test_redis:

    def __init__(self):
        self.r = redis.Redis()
        self.t = Task(self.r)

    def run(self):
        task = self.t.task
        if task:
            print(task)
            self.t.save()
