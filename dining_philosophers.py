import threading
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork, finish_flag):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.dirty_left = False
        self.dirty_right = False
        self.eat_count = 0
        self.finish_flag = finish_flag

    def run(self):
        while not self.finish_flag.is_set():
            self.think()
            self.request_forks()
            self.eat()
            self.release_forks()

    def think(self):
        print(f"Philosopher {self.index} is thinking.")
        time.sleep(0.5)

    def request_forks(self):
        print(f"Philosopher {self.index} is requesting forks.")
        self.left_fork.acquire(self.index, self.dirty_left)
        self.dirty_left = True
        self.right_fork.acquire(self.index, self.dirty_right)
        self.dirty_right = True

    def eat(self):
        print(f"Philosopher {self.index} is eating.")
        self.eat_count += 1
        time.sleep(0.5)

    def release_forks(self):
        print(f"Philosopher {self.index} is releasing forks.")
        self.left_fork.release(self.index, self.dirty_left)
        self.dirty_left = False
        self.right_fork.release(self.index, self.dirty_right)
        self.dirty_right = False

class Fork:
    def __init__(self, index):
        self.lock = threading.Condition()
        self.index = index

    def acquire(self, philosopher_index, dirty_flag):
        with self.lock:
            while dirty_flag:
                self.lock.wait()
            dirty_flag = True
            print(f"Philosopher {philosopher_index} acquired fork {self.index}.")

    def release(self, philosopher_index, dirty_flag):
        with self.lock:
            dirty_flag = False
            print(f"Philosopher {philosopher_index} released fork {self.index}.")
            self.lock.notify()

def visualize(eat_counts):
    fig, ax = plt.subplots()
    ax.bar(range(1, len(eat_counts) + 1), eat_counts)
    ax.set_xlabel('Philosopher')
    ax.set_ylabel('Number of Eats')
    ax.set_title('Eating Counts for Each Philosopher')
    plt.show()

def main():
    num_philosophers = 6
    forks = [Fork(i) for i in range(num_philosophers)]
    finish_flag = threading.Event()
    philosophers = [Philosopher(i, forks[i], forks[(i + 1) % num_philosophers], finish_flag) for i in range(num_philosophers)]

    for philosopher in philosophers:
        philosopher.start()

    time.sleep(10)  # Запускаем программу на 10 секунд (можно изменить по необходимости)
    finish_flag.set()  # Устанавливаем флаг завершения после истечения времени
    for philosopher in philosophers:
        philosopher.join()

    eat_counts = [philosopher.eat_count for philosopher in philosophers]
    print("Total Eat Counts:", eat_counts)
    visualize(eat_counts)

if __name__ == "__main__":
    main()
