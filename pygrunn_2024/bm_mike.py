def the_func(arg1, arg2):
    pass


def the_func(arg1: str, arg2: str, /):
    pass


# correct:
the_func("a", "b")

# wont work: TypeError: the_func() got some positional-only arguments passed as keyword arguments: 'arg2'
the_func("a", arg2="b")

# wont work: TypeError: the_func() got some positional-only arguments passed as keyword arguments: 'arg1, arg2'
the_func(arg1="a", arg2="b")


def the_func_kw_only(*, arg1, arg2):
    pass


def the_func_arg_only(arg1, arg2, /):
    pass


def benchmarking_args_vs_kwargs():
    """
                 min (s) 	 max (s) 	 avg (s)
    pos: 		 1.38941 	 1.72278 	 1.58808
    arg only: 	 1.34003 	 1.40825 	 1.38234
    kwarg: 		 1.72834 	 1.76344 	 1.75132
    kw only: 	 1.70626 	 1.76273 	 1.74170

    """

    nnn = 2.74669
    ooo = 2.35694

    diff_secs = nnn - ooo
    diff_secs_perc = diff_secs / ooo
    print(f"diff is {diff_secs:.2f} seconds or {diff_secs_perc:.2%}")
    diff_ns = diff_secs / 25e6 * 1e9
    print(f"this is {diff_ns:.2f}ns")
    # light speed is 1 foot per ns
    print(f"in this time light travels {diff_ns * 0.3048} meters or ")
    print(f"in this time light travels {diff_ns * 0.3048} meters or ")

    # quit()

    import timeit

    number = 25_000_000
    repeat = 10

    times_pos: [float] = timeit.repeat(
        stmt="func('hello', 'world')",
        globals={"func": the_func},
        number=number,
        repeat=repeat,
    )
    times_kwarg: [float] = timeit.repeat(
        stmt="func(arg1='hello', arg2='world')",
        globals={"func": the_func},
        number=number,
        repeat=repeat,
    )
    # times_kwarg_only: [float] = timeit.repeat(stmt="func(arg1='hello', arg2='world')", globals={'func': the_func_kw_only}, number=number, repeat=repeat)
    # times_arg_only: [float] = timeit.repeat(stmt="func('hello', 'world')", globals={'func': the_func_arg_only}, number=number, repeat=repeat)

    print("\t\t\t min (s) \t max (s) \t avg (s)")
    print(f"pos: \t\t {min(times_pos):.5f} \t {max(times_pos):.5f} \t {sum(times_pos) / len(times_pos):.5f}")
    # print(f"arg only: \t {min(times_arg_only):.5f} \t {max(times_arg_only):.5f} \t {sum(times_arg_only) / len(times_arg_only):.5f}")
    print(f"kwarg: \t\t {min(times_kwarg):.5f} \t {max(times_kwarg):.5f} \t {sum(times_kwarg) / len(times_kwarg):.5f}")
    # print(f"kw only: \t {min(times_kwarg_only):.5f} \t {max(times_kwarg_only):.5f} \t {sum(times_kwarg_only) / len(times_kwarg_only):.5f}")

    quit()
    # from memory_profiler import memory_usage
    # mem_usage = memory_usage(the_func(1, 2))
    # print('Memory usage (in chunks of .1 seconds): %s' % mem_usage)
    # print('Maximum memory usage: %s' % max(mem_usage))
    print("\nPOSITIONAL")
    print("PROFILE")
    cProfile.run(f"""the_func('hello', 'world')""")

    print("\nKWARG")
    cProfile.run(f"""the_func(arg1='hello', arg2='world')""")

    # print("RES")
    # import resource
    # start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # the_func('hello', 'world')
    # delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
    # print(delta_mem)


benchmarking_args_vs_kwargs()
