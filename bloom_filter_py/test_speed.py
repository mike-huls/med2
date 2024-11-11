import random
import time
import timeit
from typing import List

from _test_utils.timing import display_times, Timing, performance_check
from _test_utils.utils_for_testing import random_str, Timer

from bloom_filter_py.simple_py_bloomfilter_bitarray import BloomFilter as BloomPyBA
from bloomlib import BloomFilter
from bloom_filter import BloomFilter as BloomFilterPackage
from bloom_filter_py.simple_py_bf import BloomFilter as BloomPy


def test_performance_check():
    elem_count = 50_000

    bf_py = BloomPy(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
    bf_ba = BloomPyBA(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
    bf_rs = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
    bf_pg = BloomFilterPackage(max_elements=elem_count, error_rate=0.05)

    string_list = [random_str(16) for _ in range(elem_count)]

    @performance_check
    def add_stuff(_bf, item_list):
        for k in item_list:
            _bf.add(k)

    add_stuff(bf_py, string_list)
    add_stuff(bf_ba, string_list)
    add_stuff(bf_rs, string_list)
    add_stuff(bf_pg, string_list)


def test_time_add():
    """ """
    strt = time.perf_counter()
    # for elem_count in [1000]:
    for elem_count in [100, 1_000, 10_000]:
        bf_py = BloomPy(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
        bf_ba = BloomPyBA(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
        bf_rs = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
        bf_pg = BloomFilterPackage(max_elements=elem_count, error_rate=0.05)

        number = 5
        repeat = 5
        string_list = [random_str(16) for _ in range(elem_count)]

        def add_stuff_pg():
            for k in string_list:
                bf_pg.add(key=k)

        def add_stuff_py():
            for k in string_list:
                bf_py.add(item=k)

        t_py: [float] = timeit.repeat(stmt=f"func()", globals={"func": add_stuff_py}, number=number, repeat=repeat)
        t_ba: [float] = timeit.repeat(stmt=f"func({string_list})", globals={"func": bf_ba.add_bulk}, number=number, repeat=repeat)
        t_rs: [float] = timeit.repeat(stmt=f"func({string_list})", globals={"func": bf_rs.add_bulk}, number=number, repeat=repeat)
        t_pg: [float] = timeit.repeat(stmt=f"func()", globals={"func": add_stuff_pg}, number=number, repeat=repeat)

        print("\n")
        display_times(
            [
                Timing(name=f"📦 bloom-filter pkg", times=[t * 1_000 for t in t_pg], size=None),
                Timing(name=f"🐍 simple", times=[t * 1_000 for t in t_py], size=None),
                Timing(name=f"🐍 bitarray", times=[t * 1_000 for t in t_ba], size=None),
                Timing(name=f"🦀 bloomlib", times=[t * 1_000 for t in t_rs], size=None),
                # Timing(name=f'{elem_count} ints', times=[t * 1_000 for t in timings_ints], size=None),
            ],
            name=f"add_bulk (#{len(string_list)})",
            decimals=9,
        )
    print(time.perf_counter() - strt)


def test_time_contains():
    """ """
    elem_count = 10_000

    bf_py = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
    bf_rs = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)

    number = 3
    repeat = 5
    string_list = [random_str(16) for _ in range(elem_count)]
    first_string = string_list[0]

    bf_py.add_bulk(string_list)
    bf_rs.add_bulk(string_list)

    py_t_contains_string_exists: [float] = timeit.repeat(stmt=f"func('{first_string}')", globals={"func": bf_py.contains}, number=number, repeat=repeat)
    py_t_contains_string_not_exists: [float] = timeit.repeat(stmt=f"func('zz')", globals={"func": bf_py.contains}, number=number, repeat=repeat)
    rs_t_contains_string_exists: [float] = timeit.repeat(stmt=f"func('{first_string}')", globals={"func": bf_rs.contains}, number=number, repeat=repeat)
    rs_t_contains_string_not_exists: [float] = timeit.repeat(stmt=f"func('zz')", globals={"func": bf_rs.contains}, number=number, repeat=repeat)

    print("\n")
    display_times(
        [
            Timing(name=f"🐍 contains ✅", times=[t * 1_000 for t in py_t_contains_string_exists], size=None),
            Timing(name=f"🐍 contains ❌", times=[t * 1_000 for t in py_t_contains_string_not_exists], size=None),
            Timing(name=f"🦀 contains ✅", times=[t * 1_000 for t in rs_t_contains_string_exists], size=None),
            Timing(name=f"🦀 contains ❌", times=[t * 1_000 for t in rs_t_contains_string_not_exists], size=None),
            # Timing(name=f'contains int', times=[t * 1_000 for t in t_contains_int_exists], size=None),
            # Timing(name=f'contains unknown int', times=[t * 1_000 for t in t_contains_int_not_exists], size=None),
        ],
        name=f"Contains (#{len(string_list)})",
        decimals=9,
    )


def test_simple():
    """ """
    elem_count = 100

    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
    print("hashes", bloom.hash_count)
    print("bitlen", len(bloom.bit_array))

    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.01)
    bloom.add(item="1")
    bloom.contains(item="1")


def test_fp():
    """ """
    elem_count = 100

    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
    print("hashes", bloom.hash_count)
    print("bitlen", len(bloom.bit_array))

    for i in range(100):
        bloom.add(str(i))

    fp = 0
    for i in range(elem_count, elem_count * 2):
        if bloom.contains(str(i)):
            fp += 1

    print(fp)

    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.01)
    bloom.add(item="1")
    bloom.contains(item="1")
