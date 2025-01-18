import threading
import time
import random

class ReaderWriter:
    def __init__(self):
        self.count = 0                      # number of active readers
        self.r = threading.Semaphore(1)     # semaphore for readers
        self.w = threading.Semaphore(1)     # semaphore for writers

    def reader(self):
        global count
        self.r.acquire()                    # to enter critical section for reader count
        self.count += 1
        if self.count == 1:
            self.w.acquire()                # if reader is first, lock the writer
        self.r.release()                    # to exit critical section

        # simulate reading
        print(f"{threading.current_thread().name} has started reading.")
        time.sleep(random.uniform(5, 10))   # simulating reading time
        print(f"{threading.current_thread().name} has stopped reading.")

        self.r.acquire()                    # to enter critical section for reader count
        self.count -= 1
        if self.count == 0:
            self.w.release()                # if last reader, unlock the writer
        self.r.release()                    # to exit critical section

    def writer(self):
        self.w.acquire()                    # to wait for exclusive access

        # simulate writing
        print(f"{threading.current_thread().name} has started writing.")
        time.sleep(random.uniform(5, 10))   # simulating writing time
        print(f"{threading.current_thread().name} has stopped writing.")

        self.w.release()                    # to release exclusive access


if __name__ == "__main__":
    rw = ReaderWriter()

    print("Welcome to the Reader-Writer Problem!")
    print("\nChoose one of the following options: \n1. Read \n2. Write")
    
    while True:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            print(f"\nNumber of processes currently reading: {rw.count + 1}")
            threading.Thread(target = rw.reader, name = f"Reader-{random.randint(1, 100)}").start()
            
        elif choice == 2:
            print(f"\nNumber of processes currently reading: {rw.count}")
            if rw.count != 0:
                print("Wait until readers are finished reading.")
            threading.Thread(target = rw.writer, name = f"Writer-{random.randint(1, 100)}").start()
        else:
            print("Invalid choice. Please enter 1 for Read or 2 for Write.")
