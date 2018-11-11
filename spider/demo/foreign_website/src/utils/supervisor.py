# -*- coding: UTF-8 -*-
 
import os
import threading
import time


 
class Supervisor (threading.Thread):   #继承父类threading.Thread
    def __init__(self,process_name,process_script,log_path,exit_flag):
        threading.Thread.__init__(self)
        self.process_name = process_name
        self.process_script = process_script
        self.log_path = log_path
        self.exit_flag = exit_flag
    
    def check_isalive(self):
        return False if time.time() - os.stat(self.log_path).st_mtime() > 10 else True 
    
    def isRunning(self):
        try:
            proccess = os.popen('ps aux | grep %s | grep -v grep' % self.process_name).read()
            if proccess:
                if self.check_isalive(self.log_path):
                    return True
                else:
                    proc = proccess.split('\n')
                    for line in proc:
                        try:
                            print line
                            proc_id = line.split()[0]
                            os.system('kill -9 %s' % proc_id)
                        except:
                            print "kill proc occur wrong"
                    return False
            else:
                return False
        except:
            print("Check process ERROR!!!")
            return False
    
    def startProcess(self,process_script):
        try:
            
            result_code = os.system(process_script)
            if result_code == 0:
                return True
            else:
                return False
        except:
            print("Process start Error!!!")
            return False
    
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        while not self.exit_flag['exit']:
            try:
                time.sleep(30)
    
                if (self.isRunning(self.process_name)):    
                    time.sleep(30)
                else:
                    self.startProcess(self.process_script)
            except Exception,e:
                print 'wrong:' + e.message
                
 
# 创建新线程
# thread1 = Supervisor(1, "Thread-1", 1)
# thread2 = Supervisor(2, "Thread-2", 2)
# 
# # 开启线程
# thread1.start()
# thread2.start()
#  
# print "Exiting Main Thread"