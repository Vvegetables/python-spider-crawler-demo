import sys
from Test.test_spider import Test_spider, Test_charset
from Test.test_model import Test_model
from Test.test_route import Test_route
from Test.test_class import Test_request
from Test.test_redis import Test_redis



def get_help():
    a = """
        -model run test model.
        -route run test route.
        -mysql run test dbs.
        -redis run test redis.
        -spider:
            spider: run spider test;
            charset: run spider charset test;
        -class:
            request: run request test;
        --help return help.
    """
    print(a)


def test_route():
    test = Test_route()
    test.run()


def test_spider():
    test = Test_spider()
    test.run()

def test_redis():
    t = Test_redis()
    t.run()


def test_model():
    t = Test_model()
    t.run()


def test_charset():
    t = Test_charset()
    t.run()


def test_request():
    t = Test_request()
    t.run()


def Test_class_dict():
    r = {
        'request': test_request,
    }
    return r


def Test_spider_dict():
    r = {
        'spider': test_spider,
        'charset': test_charset,
    }
    return r


def test_task():
    r = {
        '-route': test_route,
        '-spider': Test_spider_dict,
        '--help': get_help,
        '-model': test_model,
        '-class': Test_class_dict,
        '-redis': test_redis,
        }
    return r


def main():
    args = sys.argv
    if len(args) >= 2:
        fir = args[1]
        r = test_task()
        task = r.get(fir, get_help)
        t = task()
        if isinstance(t, dict):
            try:
                sec = args[2]
                task = t.get(sec, get_help)
            except:
                task = get_help
            task()
    else:
        get_help()


if __name__ == '__main__':
    main()
