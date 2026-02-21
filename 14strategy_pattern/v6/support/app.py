"""Customer support handling class."""

import random
from support.ticket import SupportTicket
from typing import Callable,Optional
from dataclasses import dataclass

TicketOrderingStrategy = Callable[[list[SupportTicket]],list[SupportTicket]]

def fifo_strategy(tickets: list[SupportTicket]) -> list[SupportTicket]:
  return tickets.copy()
    
def filo_strategy(tickets: list[SupportTicket]) -> list[SupportTicket]:
  return list(reversed(tickets))

def random_strategy_creator(seed: Optional[int] = None) -> TicketOrderingStrategy:
  use_seed = None
  def random_strategy(tickets: list[SupportTicket]) -> list[SupportTicket]:
    if use_seed:
      random.seed(use_seed)
    else: 
      random.seed(seed)
    return random.sample(tickets,len(tickets))
  return random_strategy

@dataclass
class RandomOrderingStrategy:
  seed: Optional[int] = None
  def __call__(self,tickets: list[SupportTicket]) -> list[SupportTicket]:
    random.seed(self.seed)
    return random.sample(tickets, len(tickets))

class CustomerSupport:
  def __init__(self):
    self.tickets = list[SupportTicket] = []

  def add_ticket(self, ticket: SupportTicket):
    self.tickets.append(ticket)

  def process_tickets(self, processing_strategy:TicketOrderingStrategy):
    # create the ordered list of tickets
    ticket_list = processing_strategy(self.tickets)

    if len(ticket_list) == 0:
      print("There are no tickets to process. Well done!")
      return 

    # go through the tickets in the list
    for ticket in ticket_list:
      ticket.process()


    # clear the tickets list
    self.tickets = []