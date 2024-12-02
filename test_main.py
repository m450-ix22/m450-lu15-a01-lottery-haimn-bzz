"""
Integrationstests für die Hauptlogik des Projekts.
"""
import pytest
from main import main


@pytest.fixture
def input_generator():
    """
    Generator, um Eingaben für den Test zu simulieren.
    """
    def simulate_inputs(inputs):
        input_iter = iter(inputs)

        def mock_input(_):
            return next(input_iter)

        return mock_input

    return simulate_inputs


def test_main_exit(input_generator, capsys, monkeypatch):
    """Testet die Hauptfunktion mit der Exit-Option."""
    inputs = ["geheim", "Z"]
    monkeypatch.setattr("builtins.input", input_generator(inputs))
    main()
    output = capsys.readouterr().out
    assert "Lotto" in output
    assert "Beenden" in output


def test_main_money(input_generator, capsys, monkeypatch):
    """Testet die Geldtransaktion in der Hauptfunktion."""
    inputs = ["geheim", "A", "E", "10", "A", "Z"]  # Passwort, Einzahlung, Menüwahl, Beenden
    monkeypatch.setattr("builtins.input", input_generator(inputs))
    main()
    output = capsys.readouterr().out
    assert "Konto Ein- und Auszahlungen tätigen" in output
    assert "10" in output  # Überprüft, ob der Betrag korrekt verarbeitet wurde


def test_main_ticket(input_generator, capsys, monkeypatch):
    """Testet die Erstellung eines Lottoscheins."""
    inputs = ["geheim", "B", "1", "2", "3", "4", "5", "6", "3", "Z"]  # Passwort, Lottozahlen, Jokerzahl, Beenden
    monkeypatch.setattr("builtins.input", input_generator(inputs))
    main()
    output = capsys.readouterr().out
    assert "Lottotipps abgeben" in output
    assert "Dein neues Guthaben" in output