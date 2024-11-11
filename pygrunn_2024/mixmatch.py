# def len_new(x, /, *, no_duplicates=False):
def len_new(x, /, no_duplicates=False):
    if no_duplicates:
        return len(set([a for a in x]))
    return len(x)


# exactly one arg, no kwarg
print(len_new([5, 5, 5]))
print(len_new("abca"))
# exactly one arge, one kwarg
print(len_new([5, 5, 5], True))
print(len_new([5, 5, 5], no_duplicates=True))
print(len_new("abca", no_duplicates=True))
print(len_new("abca", True))


def len_new(x, /, *, no_duplicates=False):
    if no_duplicates:
        return len(set([a for a in x]))
    return len(x)


# exactly one arg, no kwarg
print(len_new([5, 5, 5]))
print(len_new("abca"))
# exactly one arge, one kwarg
print(len_new([5, 5, 5], no_duplicates=True))
print(len_new("abca", no_duplicates=True))


def create_url(*, url: str, **kwargs) -> str:
    if not kwargs:
        return url
    query_params = "&".join(f"{k}={v}" for k, v in kwargs.items())
    return f"{url}?{query_params}"


print(create_url(url="https://mikehuls.com/articles", tag="python"))


def url(base_url, /, *paths, scheme="https", **params):
    """Create a URL from a base URL and a list of paths and query parameters"""

    _url = f"{scheme}://{base_url}"

    if len(paths) > 1:
        _url += "/" + "/".join(paths)

    if len(params) > 1:
        _url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    return _url


print("____________")
print(url("www.mikehuls.com"))
print(url("www.mikehuls.com", top=100, article_id=10))
print(url("www.mikehuls.com", "articles", "python", top=100, article_id=10))
print(url("www.mikehuls.com", "articles", "python", scheme="http", top=100, article_id=10))

quit()
# fails: multiple pos args, only one allowed
# print(len_new([5, 5, 5], 'value', no_duplicates=True))  # takes 1 positional argument but 2 positional arguments (and 1 keyword-only argument) were given
# fails: too many kwargs, only one allowed
# print(len_new([5, 5, 5], no_duplicates=True, foo="bar")) # Unexptected keyword argument 'foo'
# fails: too many kwargs, wrong keyword arg
# print(len_new([5, 5, 5], test=True))                    # got an unexpected keyword argument 'test'


print("==========divide")


def divide(number, *other_numbers, omit_zero: bool = True, **kwargs):
    for num in other_numbers:
        if num == 0 and omit_zero:
            continue
        number /= num
    return number


print(divide(500, 5, 20, 2))
print(divide(500, 5, 20, 2, 0))  # 0 will be omitted
# allow fn to raise
# print(divide(500, 5, 20, 2, 0, omit_zero=False))     # ZeroDivisionError
print(divide(500, 5, 20, 2, 0, omit_zero=True, name="jo"))  #


def my_function(x, /, y, *args, z, **kwargs):
    print(x, y, z, args, kwargs)


print(
    my_function(
        "x",
        "y",
        "extra_pos1",
        "extra_pos2",
        z="z",
        aa="extra_kwarg1",
        ab="extra_kwarg1",
    )
)
quit()

# def test(x, /, *, ding):


def the_func(pos_only1, pos_only2, /, pos_or_kw1, pos_or_kw2, *ding, kw1, kw2, **extra_kw):
    # cannot be passed kwarg <-- | --> can be passed 2 ways | --> can only be passed by kwarg
    print(f"{pos_only1=}, {pos_only2=},{pos_or_kw1=}, {pos_or_kw2=}, {kw1=},{kw2=},{extra_kw=}")
    print(ding)


print(the_func(1, 2, 3, 4, 4.1, 4.2, kw1=5, kw2=6, no7=7, no8=8))
