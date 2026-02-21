"""Customer support handling class."""

import random
from support.ticket import SupportTicket
from typing import Protocol 

class TicketOrderingStrategy(Protocol):
  def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
    """Returns a ordered list of tickets."""

class FIFOOrderingStrategy:
  def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
    return tickets.copy()
    
class FILOOrderingStrategy:
  def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
    return list(reversed(tickets))

class RandomOrderingStrategy:
  def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
    return random.sample(tickets,len(tickets))

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