from dataclasses import dataclass
from transaction import Transaction
from account import Account

class Deposit:
  account: Account
  amount: int

  @property
  def transaction_details(self) -> str:
    return f"${self.amount / 100:.2f} to account {self.account.name}"
  
  def execute(self) -> None:
    self.account.deposit(self.amount)
    print(f"Deposited {self.transaction_details}")


@dataclass
class Withdrawal:
  account: Account
  amount: int

  @property
  def transaction_details(self) -> str:
    return f"${self.amount / 100:.2f} to account {self.account.name}"
  
  def execute(self) -> None:
    self.account.withdraw(self.amount)
    print(f"Withdraw {self.transaction_details}")

@dataclass
class Transfer:
  from_account: Account
  to_account: Account
  amount: int

  @property
  def transaction_details(self) -> str:
    return f"${self.amount / 100:.2f} from account {self.from_account.name} to account {self.to_account.name}"
  
  def execute(self) -> None:
    self.from_account.withdraw(self.amount)
    self.to_account.deposit(self.amount)
    print(f"Transferred {self.transaction_details}")

@dataclass
class Batch:
  commands: list[Transaction] = []

  def execute(self) -> None:
    for command in self.commands:
      command.execute()