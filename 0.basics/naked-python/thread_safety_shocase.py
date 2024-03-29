import platform
import sys
import threading


class UnsyncedBankAccount:
    """Bank account with no synchronization lock, prone to race condition."""

    def __init__(self):
        self.is_open = False
        self.balance = 0

    def get_balance(self):
        if self.is_open:
            return self.balance
        else:
            raise ValueError

    def open(self):
        self.is_open = True

    def deposit(self, amount):
        if self.is_open and amount > 0:
            self.balance += amount
        else:
            raise ValueError

    def withdraw(self, amount):
        if self.is_open and 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError

    def close(self):
        self.is_open = False


class SyncedBankAccount:
    """Bank account with synchronization strategy, thread-safe."""

    def __init__(self):
        self.is_open = False
        self.balance = 0
        self.lock = threading.Lock()

    def get_balance(self):
        with self.lock:
            if self.is_open:
                return self.balance
            else:
                raise ValueError

    def open(self):
        self.is_open = True

    def deposit(self, amount):
        with self.lock:
            if self.is_open and amount > 0:
                self.balance += amount
            else:
                raise ValueError

    def withdraw(self, amount):
        with self.lock:
            if self.is_open and 0 < amount <= self.balance:
                self.balance -= amount
            else:
                raise ValueError

    def close(self):
        self.is_open = False


def adjust_balance_concurrently(account):
    def transact():
        account.deposit(5)
        account.withdraw(5)

    # Greatly improve the chance of an operation being interrupted
    # by thread switch, thus testing synchronization effectively.
    # Feel free to tweak the parameters below to see their impact.
    try:
        sys.setswitchinterval(1e-12)
    except AttributeError:
        # Python 2 compatible
        sys.setcheckinterval(1)

    threads = []
    for _ in range(1000):
        t = threading.Thread(target=transact)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # Initialization
    unsync_account = UnsyncedBankAccount()
    unsync_account.open()
    unsync_account.deposit(1000)
    sync_account = SyncedBankAccount()
    sync_account.open()
    sync_account.deposit(1000)

    # Test unsynced bank account
    for _ in range(10):
        adjust_balance_concurrently(unsync_account)

    # Test synced bank account
    for _ in range(10):
        adjust_balance_concurrently(sync_account)

    # Report results
    print(f"Python version: {platform.python_version()}\n")
    print("Balance of unsynced account after concurrent transactions:")
    print(f"{unsync_account.balance}. Expected: 1000\n")
    print("Balance of synced account after concurrent transactions:")
    print(f"{sync_account.balance}. Expected: 1000\n")
