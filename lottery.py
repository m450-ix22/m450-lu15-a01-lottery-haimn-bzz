from numeric_input import read_int
from ticket import Ticket


def create_ticket(person):
    """
    Erzeugt ein neues Lottoticket und reduziert das Guthaben des Benutzers.
    """
    if person.balance >= 2.00:
        person.balance -= 2
        ticket = Ticket(0, [])
        select_numbers(ticket)
        print_ticket(ticket)
        print(f"Dein neues Guthaben: {person.balance:.2f}")
    else:
        print("Zuwenig Guthaben")


def select_numbers(ticket):
    """
    Erlaubt dem Benutzer, Zahlen für sein Ticket auszuwählen.
    """
    while len(ticket.numbers) < 6:
        number = read_int(f"{len(ticket.numbers) + 1}. Zahl: Geben Sie eine Zahl von 1 bis 42 ein > ", 1, 42)
        if number not in ticket.numbers:
            ticket.numbers.append(number)
        else:
            print("Diese Zahl haben Sie schon gewählt")
    ticket.joker = read_int("Jokerzahl: Geben Sie eine Zahl von 1 bis 6 ein > ", 1, 6)


def print_ticket(ticket):
    """
    Gibt das erstellte Lottoticket aus.
    """
    for count in range(1, 43):
        if count in ticket.numbers:
            print(f"{'X':>4}", end="")
        else:
            print(f"{count:4d}", end="")
        if count % 6 == 0:
            print()
    print(f"\n\nJokerzahl: {ticket.joker:2d}")