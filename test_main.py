import pytest
from numeric_input import read_int, read_float
from lottery import create_ticket, select_numbers, print_ticket
from authenticate import load_people, login
from money import transfer_money
from menu import select_menu, show_menu
from person import Person
from ticket import Ticket

@pytest.fixture
def test_person():
    """Fixture for a test Person object."""
    return Person("TestUser", "securepass", 10.0)


# Tests for numeric_input.py
def test_read_int_valid_input(monkeypatch):
    inputs = iter(["5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert read_int("Enter a number: ", 1, 10) == 5


def test_read_int_invalid_input(monkeypatch, capsys):
    inputs = iter(["15", "8"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = read_int("Enter a number: ", 1, 10)
    captured = capsys.readouterr()
    assert "Eingabe ist zu gross oder zu klein" in captured.out
    assert result == 8


def test_read_float_valid_input(monkeypatch):
    inputs = iter(["12.5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert read_float("Enter a float: ", 10.0, 20.0) == 12.5


def test_read_float_invalid_input(monkeypatch, capsys):
    inputs = iter(["25.5", "15.5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = read_float("Enter a float: ", 10.0, 20.0)
    captured = capsys.readouterr()
    assert "Eingabe ist zu gross oder zu klein" in captured.out
    assert result == 15.5


# Tests for lottery.py
def test_create_ticket_success(test_person, capsys):
    create_ticket(test_person)
    captured = capsys.readouterr()
    assert "Dein neues Guthaben" in captured.out
    assert test_person.balance == 8.0


def test_create_ticket_insufficient_balance(test_person, capsys):
    test_person.balance = 1.0
    create_ticket(test_person)
    captured = capsys.readouterr()
    assert "Zuwenig Guthaben" in captured.out


def test_select_numbers(monkeypatch):
    inputs = iter(["1", "2", "3", "4", "5", "6", "3"])  # Last "3" is duplicate to test rejection
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    ticket = Ticket(0, [])
    select_numbers(ticket)
    assert ticket.numbers == [1, 2, 3, 4, 5, 6]


# Tests for authenticate.py
def test_load_people():
    people = load_people()
    assert len(people) == 3
    assert people[0].givenname == "Inga"


def test_login(monkeypatch):
    inputs = iter(["geheim"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    person = login()
    assert person.givenname == "Inga"


# Tests for money.py
def test_transfer_money_deposit(test_person, monkeypatch):
    inputs = iter(["E", "20", "Z"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    transfer_money(test_person)
    assert test_person.balance == 30.0


def test_transfer_money_withdraw(test_person, monkeypatch):
    inputs = iter(["A", "5", "Z"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    transfer_money(test_person)
    assert test_person.balance == 5.0


# Tests for menu.py
def test_show_menu(capsys):
    show_menu()
    captured = capsys.readouterr()
    assert "Lotto" in captured.out


def test_select_menu_valid_input(monkeypatch):
    inputs = iter(["A"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    selection = select_menu()
    assert selection == "A"


def test_select_menu_invalid_input(monkeypatch, capsys):
    inputs = iter(["X", "B"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    selection = select_menu()
    captured = capsys.readouterr()
    assert "Bitte geben Sie eine gültige Wahl ein" in captured.out
    assert selection == "B"


# Integration Tests
def test_integration_create_ticket(test_person, monkeypatch, capsys):
    inputs = iter(["1", "2", "3", "4", "5", "6", "3", "4"])  # Valid ticket numbers
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    create_ticket(test_person)
    captured = capsys.readouterr()
    assert "Dein neues Guthaben" in captured.out
    assert test_person.balance == 8.0


def test_integration_transfer_money_and_ticket(test_person, monkeypatch):
    inputs = iter(["E", "20", "Z", "1", "2", "3", "4", "5", "6", "4"])  # Add money, then create ticket
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    transfer_money(test_person)
    create_ticket(test_person)
    assert test_person.balance == 26.0


if __name__ == "__main__":
    pytest.main()