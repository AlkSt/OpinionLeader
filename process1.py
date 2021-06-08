# import time
# import multiprocessing
# import concurrent.futures
# import tvk_parse

# def get_wiki_page_existence(dc): 

#     return calk()*dc

# def exec():
#     wiki_page_urls = [2,3]
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = []
#         for url in wiki_page_urls:
#             futures.append(executor.submit(get_wiki_page_existence, dc=url))
#         for future in concurrent.futures.as_completed(futures):
#             print(future.result())

# def calk():
#     time.sleep(2)
#     return [1, 1]

# def it(status,num):
#     status.value =10**num

# def worker(status, num):
#     for ib in range(10):
#         time.sleep(2)
#         it(status, num)
#         status.value += ib*num

# def freeze_support():
#     status = multiprocessing.Value('i')
#     process = multiprocessing.Process(target=tvk_parse.get_info_about_group, args=(status,187235639))
#     process.start()

#     while process.is_alive():
#         time.sleep(1)
#         print(status.value)

# if __name__ == '__main__':
#     freeze_support()

import multiprocessing, time, random

def worker_lock(lock, lst):
    """worker с использованием блокировки""" 
    # PID процесса
    pid_proc = multiprocessing.current_process().pid
    # блокируем доступ к очереди, пока складываем в нее данные
    with lock:
        for n in range(3):
            # имитируем нагрузку, для того, что бы была 
            # конкуренция доступа к общему ресурсу (очереди)
            time.sleep(random.uniform(0.01, 0.1))
            # пока доступ из других процессов заблокирован, 
            # складываем данные - кортежи (pid, n)
            lst.put((f'PID-{pid_proc}', n))


if __name__ == '__main__':
    # кол-во процессов
    PROCESSES = 4

    # создаем объект блокировки
    lock = multiprocessing.Lock()
    # создаем очередь
    queue = multiprocessing.Queue()
    
    print('\nОЧЕРЕДЬ С БЛОКИРОВКОЙ:')
    procs = []
    for _ in range(PROCESSES):
        proc = multiprocessing.Process(target=worker_lock, args=(lock, queue))
        procs.append(proc)
        proc.start()

    # ждем результатов
    [proc.join() for proc in procs]
    # получаем данные из очереди, 
    # тем самым ее освобождаем 
    while not queue.empty():
        print(queue.get())
    
    # освобождаем ресурсы
    proc.close() 

    