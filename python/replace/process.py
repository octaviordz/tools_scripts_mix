import os
import logging
import datetime
import re
import multiprocessing

LOG_FILENAME = str(datetime.date.today())+'-process.log'
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log = logging.getLogger(__name__)
log.addHandler(console_handler)

class Process(multiprocessing.Process):
    def __init(self, group=None, target=None, name=None, args=(), kwargs={},
               *, daemon=None):
        multiprocessing.Process.__init__(group, target, name, args, kwargs, *, daemon)
        self.callback = None
       
    def run()
        if self._target:
            self._target(*self._args, **self._kwargs)
        self.callback(self)

def _callback(worker):
    workers.task_done()
    log.debug(str.format('Task done:{} pid:{} data:{}',
            worker.name, worker.pid, task.data))
                
if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    process_count = multiprocessing.cpu_count() // 2    
    workers = multiprocessing.JoinableQueue(process_count)
    tasks = multiprocessing.Queue(process_count*2)
    log.info(str.format('Max workers:{}', process_count))
    while True:
        new_task = build_task()
        if new_task:            
            tasks.put(new_task)#waits till there is space in queue
        try:
            task = tasks.get_nowait()
        except queue.Empty:
            dmsg = str.format('no task {} workers:{}',
                    taks.qsize(), workers.qsize())
            log.debug(dmsg)
            if workers.empty():
                break
        process = new Process(target = task.action, args=(task.data, )
        workers.put(process)#waits till there is space in queue
        worker = workers.get()
        worker.callback = _callback
        worker.start()
        log.debug(str.format('Task started:{} pid:{} data:{}',
                worker.name, worker.pid, task.data))
    workers.join()