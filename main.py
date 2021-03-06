from re import T
from follow_bot import spotify
import threading, os, time



lock = threading.Lock()
counter = 0



class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


def safe_print(arg):
    lock.acquire()
    print(arg)
    lock.release()


def thread_follow(account):
    global counter
    obj = spotify(account)
    result = obj.follow()
    if result:
        counter += 1
        safe_print("Followed {}".format(counter))
    else:
        print(result)
        safe_print("Error")
        

def follow_user(account: str, threads: int):
    while True:
        if threading.active_count() <= threads:
            try:
                threading.Thread(target = thread_follow, args=(account, )).start()
            except Exception as e:
                print(e)
                safe_print("Error")

def thread_follow_authtoken(account: str, token: str):
    global counter 
    obj = spotify(profile=account)
    result = obj.follow(token)
    if result:
        counter += 1
        safe_print("Followed {}".format(counter))
    else:
        safe_print("Error")


def follow_user_authtoken(account):
    with open("accounts.txt", "r") as f:
        for line in f:
            try:
                threading.Thread(target = thread_follow_authtoken, args=(account, line, )).start()
            except:
                safe_print("Error")

def thread_create():
    try:
        global counter
        obj = spotify()
        result = obj.register_account()
        auth_token = obj.get_token(result)
        if auth_token != None:
            with open("accounts.txt", "a") as f:
                f.write(f"\n{auth_token}")
            counter += 1
            safe_print("Created {}".format(counter))
            
    except Exception as e:
        print(e)
        

def create_account(threads: int):
    while True:
        if threading.active_count() <= threads:
            try:
                threading.Thread(target = thread_create).start()
            except:
                safe_print("Error")


def thread_follow_playlist(playlistd):
    try:
        global counter
        obj = spotify(playlist=playlistd)
        result = obj.register_account()
        auth_token = obj.get_token(result)
        result = obj.follow_playlist()
        if result:
            counter += 1
            safe_print("Followed {}".format(counter))
        else:
            safe_print("Error")
    except Exception as e:
        print(e)
        

def follow_playlist(playlist, threads: int):
    while True:
        if threading.active_count() <= threads:
            try:
                threading.Thread(target = thread_follow_playlist, args=(playlist, )).start()
            except:
                safe_print("Error")

def clear():
    os.system("cls" if os.name == "nt" else "clear")



def main():
    print("1. Follow Accounts")
    print("2. Follow Playlist")
    print("3. Create accounts")
    print("4. Follow accounts from file")
    userinpt = int(input(""))
    clear()
    if userinpt == 1:
        threads = input("Threads: ")
        account = input("Account: ")
        follow_user(account, int(threads))
    elif userinpt == 2:
        playlist = input("Playlist: ")
        threads = input("\nThreads: ")
        follow_playlist(playlist, int(threads))
    elif userinpt == 3:
        threads = input("\nThreads: ")
        create_account(int(threads))
    elif userinpt == 4:
        account = input("Account: ")
        follow_user_authtoken(account)
    else:
        print("Invalid input"); time.sleep(1); clear(); main()
if __name__ == "__main__":
    main()