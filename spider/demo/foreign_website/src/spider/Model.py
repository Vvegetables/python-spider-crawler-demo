import logging
import MySQLdb

class Model:
    def __init__(self, form):
        self.university = form['university']
        self.en_university = form['en_university']
        self.region = form['region']
#         self.department = form['department']
        self.url = form['url']
#         self.teacher = form['teacher']
        self.title = form['title']
        self.content = form['content']

    @classmethod
    def new(cls, form):
        return cls(form)

    def save(self):
        with open('Data/data.txt', 'a') as f: #department,teacher{teacher}^^^
            msg = """
                {university}^^^
                {en_university}^^^
                {url}^^^
                {title}^^^
                {region}^^^
                {content}\n\n\n
                """.format(
                university=self.university,
                en_university=self.en_university,
#                 department=self.department,
                url=self.url,
                region=self.region,
                title = self.title,
#                 teacher=self.teacher,
                content=self.content,
            )
            logging.info(msg)
            f.write(msg)

    def db_save(self, db):
        cursor = db.cursor()
        #department,teacher
        sql = """
        insert into `t_teachers` (`university`,`en_university`,`title`, `content`, `url`,`region`)
        values (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            self.university,
            self.en_university,
#             self.department,
#             self.teacher,
            self.title,
            self.content,
            self.url,
            self.region,
        ))
