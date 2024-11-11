import dataclasses


def transfer_money(from_account: str, to_account: str, amount: int):
    print(f"Transfering ${amount} FROM {from_account} to {to_account}")

transfer_money("TO_ACCOUNT", "FROM_ACCOUNT", 9999)
# --> Transfering $9999 FROM TO_ACCOUNT to FROM_ACCOUNT

# ONLY KWARGS
def transfer_money(*, from_account: str, to_account: str, amount: int):
    print(f"Transfering ${amount} FROM {from_account} to {to_account}")


# correct:
transfer_money(from_account="1234", to_account="6578", amount=9999)

# won't work: TypeError: transfer_money() takes 0 positional arguments but 1 positional argument (and 2 keyword-only arguments) were given
# transfer_money("1234", to_account="6578", amount=9999)

# won't work: TypeError: transfer_money() takes 0 positional arguments but 3 were given
# transfer_money("1234", "6578", 9999)


# ONLY ARGS
def the_func(arg1: str, arg2: str, /):
    print(f"provided {arg1=}, {arg2=}")


def exceeds_100_bytes(x, /) -> bool:
    return x.__sizeof__() > 100


exceeds_100_bytes("a")
exceeds_100_bytes({"a"})

len(__obj="some_string")
# --> TypeError: len() takes no keyword arguments
print(len("some_string)"))
# --> 12


@dataclasses.dataclass