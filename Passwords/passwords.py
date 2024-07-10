from multiprocessing import Pool
from multiprocessing.shared_memory import SharedMemory
import multiprocessing
import threading
import os
import typing as ty
import yaml
import time


with open('config.yaml', 'r') as config_file:
    config = yaml.full_load(config_file)


CHUNK_SZ = int(1e+8)  # 100 MB
OFFSET = 100
USER_PASSWORDS_PATH = config['UserPasswordsPath']
GLOBAL_KNOWN_PASSWORDS_PATH = config['GlobalKnownPasswordsPath']
CPU_COUNT = os.cpu_count()-1


class Timer:
    def __init__(self):
        self.started = time.perf_counter()

    @property
    def elapsed(self):
        return time.perf_counter() - self.started

    def format_elapsed(self):
        return f"Elapsed time: {self.elapsed:0.1f} seconds."

    def reset(self):
        self.started = time.perf_counter()


def find_matches(data: bytes, user_passwords: ty.Set[str]):
    data = data.decode('utf-8')
    # Possible to have empty strings here.
    ss = set(data.split('\n'))
    found = ss & user_passwords
    return found


class FindMatches:
    def __init__(self):
        self.sema = threading.BoundedSemaphore(CPU_COUNT)

    def run(self, user_passwords: ty.Set[str]):
        with Pool(CPU_COUNT) as pool:
            with open(GLOBAL_KNOWN_PASSWORDS_PATH, 'rb') as file:
                timer = Timer()
                chunks_read = 0
                while True:
                    s = file.read(CHUNK_SZ + OFFSET)
                    chunks_read += 1
                    if chunks_read % (2*CPU_COUNT) == 0:
                        print('Chunks Read:', chunks_read, timer.format_elapsed())
                    if len(s) == CHUNK_SZ + OFFSET:
                        file.seek(-OFFSET, 1)
                    else:
                        break
                    # can be a couple of callbacks
                    self.sema.acquire()
                    pool.apply_async(find_matches,
                                     args=(s, user_passwords),
                                     callback=self.on_success,
                                     error_callback=self.on_error)
            pool.close()
            pool.join()

    def on_success(self, res):
        self.sema.release()
        if res:
            print('Found passwords:', res)

    def on_error(self, ex):
        self.sema.release()
        print(ex)


def find_matches_shm_worker(shm_name: str, user_passwords: ty.Set[str]):
    shm = SharedMemory(shm_name)
    data = shm.buf.tobytes().decode('utf-8')
    # Probably a new object is created during decoding.
    shm.close()
    shm.unlink()
    # Possible to have empty strings here.
    ss = set(data.split('\n'))
    found = ss & user_passwords
    return found


def find_matches_shm(chunks_read = 0):
    def on_success(res):
        sema.release()
        if res:
            print('Found passwords:', res)

    def on_error(ex):
        sema.release()
        print(ex)

    user_passwords = read_user_passwords()
    sema = threading.BoundedSemaphore(CPU_COUNT)
    with Pool(CPU_COUNT) as pool:
        with open(GLOBAL_KNOWN_PASSWORDS_PATH, 'rb') as file:
            timer = Timer()
            if chunks_read > 0:
                file.seek(CHUNK_SZ*chunks_read, 1)
            while True:
                s = file.read(CHUNK_SZ + OFFSET)
                chunks_read += 1
                if chunks_read % (2*CPU_COUNT) == 0:
                    print('Chunks Read:', chunks_read, timer.format_elapsed())
                if len(s) == CHUNK_SZ + OFFSET:
                    file.seek(-OFFSET, 1)
                else:
                    break
                # can be a couple of callbacks
                sema.acquire()
                shm = SharedMemory(create=True, size=len(s))
                shm.buf[:] = s
                pool.apply_async(find_matches_shm_worker,
                                 args=(shm.name, user_passwords),
                                 callback=on_success,
                                 error_callback=on_error)
                shm.close()
        pool.close()
        pool.join()



def try_read_all():
    with open(GLOBAL_KNOWN_PASSWORDS_PATH) as file:
        while True:
            s = file.read(CHUNK_SZ)
            if not s:
                break
            s = s[-OFFSET:]
            s = s.split('\n')
            if len(s) > 0:
                s = s[1].strip()
                print(s)


def print_config():
    print(config)


def read_user_passwords() -> ty.Set[str]:
    with open(USER_PASSWORDS_PATH) as file:
        s = file.read()
        s = s.split('\n')
        s = set(item.strip() for item in s if item)
        return s


def print_user_passwords():
    s = read_user_passwords()
    print(s)


def find_matches_sequencial():
    """
    Takes very long time in sequenctial process.
    """
    user_passwords = read_user_passwords()
    with open(GLOBAL_KNOWN_PASSWORDS_PATH, 'rb') as file:
        chunks_read = 0
        while True:
            data = file.read(CHUNK_SZ + OFFSET)
            chunks_read += 1
            if chunks_read % (2 * CPU_COUNT) == 0:
                print('Chunks Read:', chunks_read)
            if len(data) == CHUNK_SZ + OFFSET:
                file.seek(-OFFSET, 1)
            else:
                break
            data = data.decode('utf-8')
            # Possible to have empty strings here.
            ss = set(data.split('\n'))
            found = ss & user_passwords
            if found:
                print('Found passwords:', found)


# try_read_all()
# FindMatches().run(read_user_passwords())
# print_config()
# print_user_passwords()
# find_matches_sequencial()

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    find_matches_shm(490)