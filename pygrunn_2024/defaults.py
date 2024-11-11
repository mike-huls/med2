from typing import List, Dict


def register_participant(event_name, participant, registered_participants=[]) -> List:
    registered_participants.append((event_name, participant))
    return registered_participants


event_a = register_participant(event_name="Event A", participant="Alice")
print(event_a)  # >>> [('Event A', 'Alice')]
event_b = register_participant(event_name="Event B", participant="Bob")
print(event_b)  # >>> [('Event A', 'Alice'), ('Event B', 'Bob')]


def register_participant(event_name, participant, registered_participants=None) -> List:
    if registered_participants is None:
        registered_participants = []
    registered_participants.append((event_name, participant))
    return registered_participants


event_a = register_participant(event_name="Event A", participant="Alice")
print(event_a)  # >>> [('Event A', 'Alice')]
event_b = register_participant(event_name="Event B", participant="Bob")
print(event_b)  # >>> [('Event B', 'Bob')]

quit()


def add_user_to_document(username: str, document_users: Dict[str, bool] = {}) -> Dict:
    if username not in document_users:
        document_users[username] = True
    return document_users


document_a = {}
document_a = add_user_to_document(username="alice", document_users=document_a)
print(document_a)

document_b = add_user_to_document(username="bob")
print(document_b)
print(add_user_to_document(username="alice"))

quit()


my_func(["a dog", "a cat"])
print("JOJOJO")
my_func(["some guy"])


# list, dict, set most common
