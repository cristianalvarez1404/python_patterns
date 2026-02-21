"""Support ticket handling example."""

from support.app import CustomerSupport,fifo_strategy,filo_strategy,random_strategy_creator,RandomOrderingStrategy
from support.ticket import SupportTicket

def black_hole_stategy(tickets:list[SupportTicket]) -> list[SupportTicket]:
  return []

def main():
  # create the application
  app = CustomerSupport()

  # register a few tickets
  app.add_ticket(SupportTicket("John Smith", "My computer makes strange sounds!"))
  app.add_ticket(SupportTicket("Linus Sebastian", "I can't upload any videos, please help."))
  app.add_ticket(SupportTicket("Codes", "VSCode doesn't automatically solve my bugs."))

  # process the tickets
  app.process_tickets(random_strategy_creator(seed=1))

if __name__ == "__main__":
  main()