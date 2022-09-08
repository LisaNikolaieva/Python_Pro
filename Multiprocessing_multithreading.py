import logging
import threading
import time

from multiprocessing import Process, Manager


def thread_function(n, a, b, return_dict):
    s = 0
    for itm in range(a, b):
        a1 = f'{itm:06}'
        if (int(a1[0]) + int(a1[1]) + int(a1[2])) == (int(a1[3]) + int(a1[4]) + int(a1[5])):
            s += 1
            # print(f'The happy ticket: {itm}')
    print(f'{n}: number of happy tickets {s}')
    return_dict[n] = s


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    manager = Manager()
    return_dict = manager.dict()

    ##################### Threading #######################
    # x = threading.Thread(target=thread_function, args=(1, 1, 250000, return_dict))
    # y = threading.Thread(target=thread_function, args=(2, 250001, 500000, return_dict))
    # z = threading.Thread(target=thread_function, args=(3, 500001, 750000, return_dict))
    # r = threading.Thread(target=thread_function, args=(4, 750001, 999999, return_dict))

    ##################### Processing ######################
    x = Process(target=thread_function, args=(1, 1, 250000, return_dict))
    y = Process(target=thread_function, args=(2, 250001, 500000, return_dict))
    z = Process(target=thread_function, args=(3, 500001, 750000, return_dict))
    r = Process(target=thread_function, args=(4, 750001, 999999, return_dict))

    time_start = time.time()

    x.start()
    y.start()
    z.start()
    r.start()

    x.join()
    y.join()
    z.join()
    r.join()

    time_finish = time.time()

    print(f">>>>>>>>>>>>>>>>> Running time: {time_finish - time_start}")
    print(f'>>>>>>>>>>>>>>>>> The total number of happy tickets: {sum(return_dict.values())}')
