from Model import DBsession, Data, Sql, CompletedUniversity


class Test_model:

    def test_delete_data(self):
        s = DBsession()
        d = s.query(Data).filter_by(department='测试orm').first()
        if d:
            s.delete(d)
            print('delete')
        else:
            print(f'data doesnt exit')
        s.commit()
        s.close()

    def test_find_data(self):
        s = DBsession()
        d = s.query(Data).filter_by(department='测试orm', university='测试orm').first
        if d:
            print(f'{d} exit, test success')
        else:
            print('test fail')
        s.close()

    def test_add_data(self):
        s = DBsession()
        d = Data(
            teacher='测试',
            university='测试orm',
            department='测试orm',
            content='测试orm',
            url='https://www.baidu.com/s?ie=UTF-8&wd=seleunim',
        )
        s.add(d)
        print(f'add {d}')
        s.commit()
        s.close()

    def test_with_sql(self):
        with Sql() as s:
            d = s.query(Data).filter_by(department='测试orm').first()
            print(d.department)

    def test_completed_university_model(self):
        filepath = 'Model/a.txt'
        CompletedUniversity.save_from_txt(filepath)


    def run(self):
        # self.test_add_data()
        # self.test_find_data()
        # self.test_delete_data()
        # self.test_find_data()
        # self.test_with_sql()
        self.test_completed_university_model()
