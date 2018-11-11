import json
# from my_Model import myDB
from my_Model import CompletedUniversity, Sql

class Task:

    def __init__(self, client):
        self.t = client.rpop('task')

    @property
    def task(self):
        if self.t is None:
            return None
        task = self.t.decode()
        task = task.replace('\'', '\"')
        task = json.loads(task)
        return task

    def save(self):
        data = self.t.decode()
        data = eval(data)
#         sql = "insert into t_teachers(university,department,url) values({university},{department},{url})".format(**data)
#         myDB.data_execute(sql)
        with Sql() as s:
            u = s.query(CompletedUniversity).filter_by(url=data['url']).first()
            if not u:
                d = CompletedUniversity(
                    url=data['url'],
                    university=data['university'],
                    region = data['region'],
                    en_university=data['en_university'],
#                     department=data['department'],
                    
                )
                s.add(d)
