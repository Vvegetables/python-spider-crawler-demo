from spider.Schedule import Schedule
from utils.util import get_list_first_name

class Test_spider:

    def __init__(self):
        self.task = dict(
            url='http://www.ues.pku.edu.cn/more_teacher.php?cid=31&istype=1',
            university='北京大学',
            department='城市与环境学院',
        )

    def run(self):
        list_first_name = get_list_first_name('Data/first_name.txt')
        self.task.update(
            list_first_name=list_first_name,
        )
        a = Schedule(**self.task)
        a.run()


class Test_charset(Test_spider):

    def __init__(self):
        super(Test_charset, self).__init__()
        self.task.update(
            url='http://faculty.ecnu.edu.cn/search/teacherList.faces?siteId=10&pageId=0&nodeId=19',
            university='华东师范大学',
            department='人文社会科学学院中国语言文学系',
        )
