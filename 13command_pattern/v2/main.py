from banking.bank import Bank
from banking.commands import Batch, Deposit, Transfer, Withdrawal
from banking.controller import BankController

def main() -> None:

  #create a bank
  bank = Bank()

  #create a bank controller
  controller = BankController()

  #create some accounts
  account1 = bank.create_account("user1")
  account2 = bank.create_account("Google")
  account3 = bank.create_account("Microsoft")

  controller.register(Deposit(account1, 100000))

  controller.register(
    Batch(
      commands= [
        Deposit(account2, 10000),
        Deposit(account3, 10000),
        Transfer(from_account=account2, to_account=account1, amount=50000)
      ]
    )    
  )

  #controller.register(Withdrawal(account1, 150000))
  
  bank.clear_cache()
  controller.compute_balances()
