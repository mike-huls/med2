
### Only show logs if an exception occurred
##### Breadcrumbs


This article shows you how to show you how to use the standard Python logging library to show you the breadcrumbs leading up to an error.
That's right, we'll only log out logger.debug messages _if_ an exception occurred.

The main reason for this is to prevent logging too much. You can prevent a lot of I/O writing logs to a file or sending it over HTTP to an endpoint if you only send the logs that detail what happened before an exception ocurred.
IN pseudo-code:

This will not log anything:
```python
def divide(a, b):
        
    logger.debug("starting to process")                     # <-- won't get logged since there are nog errors
    try:
        logger.debug(f"about to divide {a} by {b}")          # <-- won't get logged since there are nog errors
        return(a / b)
    except Exception as e:
        logger.error(f"Something went wrong: {e}")
divide(a=10, b=2)
```

This will print out all the debug logs since we're dividing 10 by 0
```python
def divide(a, b):
        
    logger.debug("starting to process")                     # <-- won't get logged since there are nog errors
    try:
        logger.debug(f"about to divide {a} by {b}")          # <-- won't get logged since there are nog errors
        return(a / b)
    except Exception as e:
        logger.error(f"Something went wrong: {e}")
divide(a=10, b=0)
```



### Set up a function to use
Below are our functions. As you'll see there are two `debug` logs; one in the `divide` function, the other one is in the `try` block right before we call the `divide` function.
We only want to see these two logs if there is an error in the `divide` function, which will be the case if we divide by 0 e.g. 

```python
def divide(a, b):
    logger.debug(f"Dividing [{a}] by [{b}]")
    return a / b


for value in [1, 2, 3, 4, 5, 6, 7, 8, 9, 'not a number', 0]:
    try:
        logger.debug(f"start dividing..")
        res = divide(a=10, b=value)
    except Exception as e:
        logger.error(f"❌An exception occurred: {e}")

```

### High-over solution
We'll solve this problem by configuring our logger. We'll add two handlers. 
The first will be a regular streaming handler that is responsible for displaying the logs in our console. 
This will have a loglevel of `INFO`, which means that it will ignore all `DEBUG` logs.

Second, we will regsiter a `MemoryHandler` on the streaming handler. 
This handler will act as a buffer, "remembering" up to a certain number of logs. 
The memory_handler will also be configured with a `flushLevel` of `ERROR`. 
This means that if the memory_handler detects that the stream_handler logs a message with the `ERROR` severity, it will flush all "remembered" logs to the stream_handler, which will display it for us!

After each value we'll clear the buffer of the memory_handler so that it can be filled with new logs.
Let's see what this looks like in code.


### Setup logger and handlers
First we'll create a logger and set up two handlers.  
```python
# Create logger and formatter for a nicer message
logger = logging.getLogger("my_logger")
formatter = logging.Formatter(fmt="%(levelname)-7s ⏱️%(asctime)s  📍%(funcName)12s:%(lineno)-2s  💌%(message)s", datefmt="%H:%M:%S"
                              )
# Add stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)  # Only INFO and above will be shown normally
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Add memory handler
memory_handler = MemoryHandler(capacity=100, target=stream_handler, flushLevel=logging.ERROR)
memory_handler.setFormatter(formatter)
logger.addHandler(memory_handler)
```
In the code above you'll see the two handlers. As detailed, the memory_handler is configured to have the stream_handler as a target and a flushLevel of `ERROR`.
Also notice the capacity; this will make sure that it does not keep too many logs in memory.


### Small modification to our function
After each pass we'll need to clear the buffer. This will prevent displaying logs that belong to values `1` or `2` e.g. when we want to flush records corresponding to `'not a number'`
This is what the code will look like:


```python
for value in [1, 2, 3, 4, 5, 6, 7, 8, 9, 'not a number', 0]:
    try:
        logger.debug(f"start dividing..")
        res = divide(a=10, b=value)
    except Exception as e:
        logger.error(f"❌An exception occurred: {e}")
    finally:
        memory_handler.buffer.clear()
```

And this is what the output will look like:
```text
ERROR   ⏱️17:07:03  📍        main:44  💌❌An exception occurred: unsupported operand type(s) for /: 'int' and 'str'
DEBUG   ⏱️17:07:03  📍        main:41  💌start dividing..
DEBUG   ⏱️17:07:03  📍      divide:32  💌Dividing [10] by [not a number]
ERROR   ⏱️17:07:03  📍        main:44  💌❌An exception occurred: unsupported operand type(s) for /: 'int' and 'str'
ERROR   ⏱️17:07:03  📍        main:44  💌❌An exception occurred: division by zero
DEBUG   ⏱️17:07:03  📍        main:41  💌start dividing..
DEBUG   ⏱️17:07:03  📍      divide:32  💌Dividing [10] by [0]
ERROR   ⏱️17:07:03  📍        main:44  💌❌An exception occurred: division by zero
```

With explanation:
```text
# First value 1 is processed; no logs
# Next value 3 is processed; no logs
# The logs below belong to value 'not a number'
ERROR   ⏱️17:07:03  📍        main:44  💌❌An exception occurred: unsupported operand type(s) for /: 'int' and 'str'
DEBUG   ⏱️17:07:03  📍        main:41  💌start dividing..
DEBUG   ⏱️17:07:03  📍      divide:32  💌Dividing [10] by [not a number]
ERROR   ⏱️17:07:03  📍        main:44  💌❌An exception occurred: unsupported operand type(s) for /: 'int' and 'str'
# The logs below belong to value 0
ERROR   ⏱️17:07:03  📍        main:44  💌❌An exception occurred: division by zero
DEBUG   ⏱️17:07:03  📍        main:41  💌start dividing..
DEBUG   ⏱️17:07:03  📍      divide:32  💌Dividing [10] by [0]
ERROR   ⏱️17:07:03  📍        main:44  💌❌An exception occurred: division by zero

```
As you see the exception-log gets logged twice because it will flush itself. All in all we have a nice trail of breadcrumbs that leads us to our error.

# Conclusion
With this logging setup we can limit the number of logs that we show have to process. This will 