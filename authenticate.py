from person import Person


def login():
    """
    Simuliert einen Login-Prozess und gibt den angemeldeten Benutzer zurück.
    """
    people_list = load_people()
    while True:
        password = input("Passwort > ")
        for person in people_list:
            if person.password == password:
                return person
        print("Passwort falsch")


def load_people():
    """
    Erstellt eine Liste von Benutzerobjekten.
    """
    return [
        Person("Inga", "geheim", 14.0),
        Person("Peter", "secrät", 7.0),
        Person("Beatrice", "passWORT", 23.0),
    ]