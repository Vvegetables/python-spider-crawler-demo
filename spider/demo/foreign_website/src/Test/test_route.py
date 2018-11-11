import requests
from Model import DBsession, Data

class Test_route:

    def create_test_data(self):
        s = DBsession()
        l = []
        for i in range(100):
            data = Data(
                teacher='测试{}'.format(i),
                university='测试orm',
                department='测试orm',
                content='测试orm',
            )
            l.append(data)
        s.bulk_save_objects(l)
        s.commit()
        s.close()

    def run(self):
        self.create_test_data()
