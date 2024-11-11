from pathlib import Path


# 1. One endpoint; pass url positionally,
def create_url(url, scheme="https") -> str:
    # Clean and create base url
    url = url.removesuffix("/")
    _url = f"{scheme}://{url}"

    return _url


# https://www.mikehuls.com
print(create_url("www.mikehuls.com"))
# http://localhost:8000
print(create_url("localhost:8000", scheme="http"))


# Take a little inspiration from pathlib
my_path = Path("c:/", "some", "folder", "my_file.py")

# c:\some\folder\my_file.py
print(my_path)


# Add create the path
def create_url(url, *args, scheme="https") -> str:
    # Clean and create base url
    url = url.removesuffix("/")
    _url = f"{scheme}://{url}"

    # Add path
    for path in args:
        _url += f"/{path}"

    return _url


# https://www.mikehuls.com/articles
print(create_url("www.mikehuls.com", "articles"))
# https://www.mikehuls.com/articles/python/design
print(create_url("www.mikehuls.com", "articles", "python", "design"))
# http://localhost:8000/articles
print(create_url("localhost:8000", "articles", scheme="http"))


# Add query parameters
def create_url(url, *args, scheme="https", **kwargs) -> str:
    # Clean and create base url
    url = url.removesuffix("/")
    _url = f"{scheme}://{url}"

    # Add path
    for path in args:
        _url += f"/{path}"

    # Add query params
    if len(kwargs) > 0:
        _url += "?"
        _url += "&".join(f"{k}={v}" for k, v in kwargs.items())

    return _url


# https://www.mikehuls.com/articles?tag=design
print(create_url("www.mikehuls.com", "articles", tag="design"))
# https://www.mikehuls.com/articles/python/design?tag=design&subject=functions
print(create_url("www.mikehuls.com", "articles", "python", "design", tag="design", subject="functions"))
# http://localhost:8000/articles?tag=design
print(create_url("localhost:8000", "articles", scheme="http", tag="design"))


print(create_url("www.mikehuls.com", "articles", "2024"))
print(create_url("localhost:8000", scheme="http"))
print(create_url("localhost:8000", "articles", scheme="http"))
print(create_url("localhost:8000", "articles", scheme="http", tag="design", subject="functions"))
print(create_url("www.mikehuls.com", "articles", tag="design", subject="functions"))


def create_url(url, /, *args, scheme="https", **kwargs) -> str:
    # Clean and create base url
    url = url.removesuffix("/")
    _url = f"{scheme}://{url}"

    # Add path
    for path in args:
        _url += f"/{path}"

    # Add query params
    if len(kwargs) > 0:
        _url += "?"
        _url += "&".join(f"{k}={v}" for k, v in kwargs.items())

    return _url


print(create_url("www.mikehuls.com"))
print(create_url("www.mikehuls.com", "articles", "2024"))
print(create_url("localhost:8000", scheme="http"))
print(create_url("localhost:8000", "articles", scheme="http"))
print(create_url("localhost:8000", "articles", scheme="http", tag="design", subject="functions"))
print(create_url("www.mikehuls.com", "articles", tag="design", subject="functions"))
print(create_url("articles", tag="design", subject="functions"))


def create_url(url, /, *args, scheme="https", **kwargs) -> str:
    _url = f"{scheme}://{url}"
    if len(args) > 1:
        _url += "/" + "/".join(args)

    if len(kwargs) > 1:
        _url += "/" + "/".join(kwargs)

    return _url


print(create_url("www.mikehuls.com"))
print(create_url("localhost:8000", scheme="http"))
print(create_url("localhost:8000", "some_other_arg", scheme="http", some_other="kwarg"))


create_url(ur)
