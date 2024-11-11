import cProfile
import dis
import json
import typing


def article_title():
    the_func("hello", "world")

    the_func(arg1="hello", arg2="world")


def parameters_and_args():
    def the_func(arg1: str, arg2: str):
        print(f"provided {arg1=} and {arg2=}")

    the_func("hello", "world")


def ways_of_passing_args():
    def the_func(arg1: str, arg2: str):
        print(f"provided {arg1=} and {arg2=}")

    the_func("hello", arg2="world")


def unpack_args():
    # unpacking
    def multiply(a, b, *args):
        result = a * b
        for arg in args:
            result = result * arg
        return result

    print(multiply(2, 3))
    print(multiply(3, 3, 2))


def unpack_kwargs():
    # unpacking
    def introduce(firstname, lastname, **kwargs):
        introduction = f"I am {firstname} {lastname}"
        for key, value in kwargs.items():
            introduction += f" my {key} is {value} "
        return introduction

    print(introduce(firstname="mike", lastname="huls"))
    print(introduce(firstname="mike", lastname="huls", age=33, website="mikehuls.com"))


def force_only_kwargs():
    # How to make my function accept only kwargs?

    # the asterisk removes all uncaught positional arguments.
    # Think of it like this: it's like *args but the args part is missing.
    # So instead of storing all left-over positional args in the args variable it just voids them
    def transfer_money(*, from_account: str, to_account: str, amount: int):
        print(f"Transfering ${amount} FORM {from_account} to {to_account}")

    # Notice that the first call fails; TypeError: the_func() takes 0 positional arguments but 2 were given
    # the_func('pos1', 'pos2')
    # this call will succeed.
    transfer_money(from_account="1234", to_account="6578", amount=9999)
    # won't work:
    # transfer_money('1234', to_account='6578', amount=9999)
    # transfer_money('1234', '6578', 9999)

    # Here you see that LEFTOVER uncaught positional arguments get gobbled up.
    def the_func(just1: str, *, arg1: str, arg2: str):
        print(f"provided {just1=} {arg1=}, {arg2=}")

    # Notice that the first call fails; TypeError: the_func() takes 0 positional arguments but 2 were given
    # the_func('num0', 'num1', 'num2')
    # this call will succeed.
    the_func("num0", arg1="num1", arg2="num2")


def force_only_args():
    # How to make my function only accept positional args?

    # anything before the slash must be an arg

    # the bare slash removes all uncaught kw arguments.
    # A / means that all preceding parameters are positional-only parameters.
    # Positional-only parameters before a / cannot be passed as name=value when calling the function.
    # def the_func(arg1:str, arg2:str, /, kwarg1:str):
    #     print(f'provided {arg1=}, {arg2=} {kwarg1=}')
    def the_func(arg1: str, arg2: str, /):
        print(f"provided {arg1=}, {arg2=}")

    # Notice that these will fail:; TypeError: the_func() got some positional-only arguments passed as keyword arguments: 'arg1, arg2'
    # the_func(arg1='num1', arg2='num2')
    the_func("num1", arg2="num2")  # the_func('pos1', arg2='pos2', kwarg1='pos3')
    # this call will succeed.
    the_func("num1", "num2")
    the_func("pos1", "pos2")


def only_args_or_kwargs():
    #

    def the_func(pos_only1: str, pos_only2: str, /, *, kw_only: str):
        print(f"{pos_only1=}, {pos_only2=}, {kw_only=}")

    # this succeeds
    the_func("pos1", "pos2", kw_only="kwarg1")

    # will fail: pos2 can only be passed positionally
    # the_func('pos1', pos_only_2='pos2', kw_only='kwarg1', some_other_kwarg='kwarg2')

    # Will fail: passed one too many positional arg (pos3)
    # the_func('pos1', 'pos2', 'pos3', kw_only='kwarg1')

    # When to use this?
    # e.g: when the order of the first two arguments are irrelevant but cannot be mixed up with the 3d:
    def calculate_average(article_price: float, number_of_articles: int, /, *, num_of_decimals: int):
        return round((article_price * number_of_articles) % num_of_decimals)

    print("res", calculate_average(4.4134, 55, num_of_decimals=4))


def only_star_args_and_a_kwarg():
    #

    # def exceeds_100_bytes(x, /) -> bool:
    #     return x.__sizeof__() > 100
    def exceeds_100_bytes(*args) -> bool:
        for a in args:
            if a.__sizeof__() > 100:
                return True
        return False

    def the_func(*args, max_bytes: int):
        for thing in args:
            size_in_bytes = thing.__sizeof__()
            too_large = size_in_bytes >= max_bytes
            print(f"{thing} is {size_in_bytes} bytes, this is{'' if too_large else ' not'} too large")

    # this succeeds
    # the_func('a', {'a'}, ['a'], max_bytes=100)

    print(exceeds_100_bytes("a"))
    print(exceeds_100_bytes("a", {"a"}))

    # will fail: pos2 can only be passed positionally
    # the_func('pos1', pos_only_2='pos2', kw_only='kwarg1', some_other_kwarg='kwarg2')

    # Will fail: passed one too many positional arg (pos3)
    # the_func('pos1', 'pos2', 'pos3', kw_only='kwarg1')

    # When to use this?
    # e.g: when the order of the first two arguments are irrelevant but cannot be mixed up with the 3d:
    # def calculate_average(article_price:float, number_of_articles:int, /, *, num_of_decimals:int):
    #     return round((article_price * number_of_articles) % num_of_decimals)
    # print('res', calculate_average(4.4134, 55, num_of_decimals=4))


def combination():
    def the_func(
        pos_only1: str,
        pos_only2: str,
        /,
        pos_or_kw1: str = None,
        pos_or_kw2: str = None,
        *args,
        kw_only: str = None,
        **kw,
    ):
        print(f"{pos_only1=}, {pos_only2=}, {pos_or_kw1=}, {pos_or_kw2=}, {args=}, {kw_only=}, {kw=}")

    the_func("num1", "num2", pos_or_kw1="pk1", pos_or_kw2="pk2")
    the_func("num1", "num2", "pk1", pos_or_kw2="pk2")
    the_func(
        "num1",
        "num2",
        "pk1",
        "pk2",
        "*args1",
        "*args2",
        kw_only="kwonly1",
        extra_kw1="extrakw1",
        extra_kw2="extrakw2",
    )


def all():
    def the_func(pos_only1, pos_only2, /, pos_or_kw1, pos_or_kw2, *, kw1, kw2, **extra_kw):
        # cannot be passed kwarg   <-- | --> can be passed 2 ways | --> can only be passed by kwarg
        print(f"{pos_only1=}, {pos_only2=}, {pos_or_kw1=}, {pos_or_kw2=}, {kw1=}, {kw2=}, {extra_kw=}")

    # works (pos_or_kw1 & pow_or_k2 can be passed positionally and by kwarg)
    the_func("pos1", "pos2", "pk1", "pk2", kw1="kw1", kw2="kw2")
    the_func("pos1", "pos2", pos_or_kw1="pk1", pos_or_kw2="pk2", kw1="kw1", kw2="kw2")
    the_func(
        "pos1",
        "pos2",
        pos_or_kw1="pk1",
        pos_or_kw2="pk2",
        kw1="kw1",
        kw2="kw2",
        kw_extra1="extra_kw1",
    )  # extra kwarg

    # doesnt work, (pos1 and pos2 cannot be passed with kwarg)
    # the_func(pos_only1='pos1', pos_only2='pos2', pos_or_kw1='pk1', pos_or_kw2='pk2', kw1='kw1', kw2='kw2')

    # doesnt work, (kw1 and kw2 cannot be passed positionally)
    # the_func('pos1', 'pos2', 'pk1', 'pk2', 'kw1', 'kw2')


def extending_len_pos_kwarg():
    def len_new(x, /, *, no_duplicates=False):
        if no_duplicates:
            return len(list(set([a for a in x])))
        return len(x)

    print(len_new("aabbcc", no_duplicates=False))
    print(len_new("aabbcc", no_duplicates=True))
    print(len_new([1, 1, 2, 2, 3, 3], no_duplicates=False))
    print(len_new([1, 1, 2, 2, 3, 3], no_duplicates=True))

    #
    # print(len_new(x=[1, 1, 2, 2, 3, 3]))
    print(len_new([1, 1, 2, 2, 3, 3], True))


if __name__ == "__main__":
    # pos_and_kwarg()
    # pos_multiple()
    # kwarg_multiple()
    # forbid_positional_args()
    # forbid_kw_args()
    # combination()
    # only_args_or_kwargs()
    # benchmarking_args_vs_kwargs()
    # unpack_args()
    # unpack_kwargs()
    # force_only_kwargs()
    # force_only_args()
    # only_star_args_and_a_kwarg()
    # only_args_or_kwargs()
    # all()
    extending_len_pos_kwarg()

    def the_func(pos_only, /, pos_or_kw, *, kw_only, **kwargs):
        print(pos_only, pos_or_kw, kw_only, kwargs)
