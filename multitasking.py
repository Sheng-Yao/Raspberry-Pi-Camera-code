import multiprocessing
import time

def fun1(num):
    print("Start " + num)
    time.sleep(2)
    print("End " + num)

if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=fun1, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        # this will wait the process to done then proceed the next line
        p.join()

# multiprocessing with Raspberry Pi
# import multiprocessing

# def square(n):
#     return n * n

# if __name__ == '__main__':
#     with multiprocessing.Pool(processes=4) as pool:
#         results = pool.map(square, range(10))
#     print(results)

