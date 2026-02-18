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

  def undo(self) -> None:
    self.account.withdraw(self.amount)
    print(f"Undid deposit of {self.transaction_details}")

  def redo(self) -> None:
    self.account.deposit(self.amount)
    print(f"Redid deposit of {self.transaction_details}")

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

  def undo(self) -> None:
    self.account.deposit(self.amount)
    print(f"Undid withdrawal of {self.transaction_details}")

  def redo(self) -> None:
    self.account.deposit(self.amount)
    print(f"Redid withdrawal of {self.transaction_details}")

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

  def undo(self) -> None:
    self.to_account.withdraw(self.amount)
    self.from_account.deposit(self.amount)
    print(f"Undid transfer of {self.transaction_details}")

  def redo(self) -> None:
    self.from_account.withdraw(self.amount)
    self.to_account.deposit(self.amount)
    print(f"Redid transfer of {self.transaction_details}")

@dataclass
class Batch:
  commands: list[Transaction] = []

  def execute(self) -> None:
    completed_commands = list[Transaction] = []
    try:
      for command in self.commands:
        command.execute()
        completed_commands.append(command)
    except ValueError as error:
      print(f"Command error: {error}")
      for command in reversed(self.commands):
        command.undo()

  def undo(self) -> None:
    for command in reversed(self.commands):
      command.undo()

  def redo(self) -> None:
    for command in self.commands:
      command.redo()