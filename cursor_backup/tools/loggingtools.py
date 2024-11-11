import logging

import coloredlogs


logger = logging.getLogger(name="test")

# Define the custom log level styles
log_styles = {
    "debug": {"color": "green"},
    "info": {"color": "blue"},  # Set INFO messages to blue
    "warning": {"color": "yellow"},
    "error": {"color": "red"},
    "critical": {"color": "red", "bold": True},
}
field_styles = {
    "name": {"color": "white"},
    "thread": {"color": "white"},
    "lineno": {"color": "white"},
    "module": {"color": "white"},
    "asctime": {"color": "white"},
    "hostname": {"color": "white"},
    "levelname": {"color": "white", "bold": True},
    "programname": {"color": "white"},
    "threadName": {"color": "white"},
}
# Configure coloredlogs with the custom styles
coloredlogs.install(
    level="DEBUG",
    logger=logger,
    fmt=f"[%(name)s] %(thread)-7s %(asctime)s %(module)-12s %(lineno)-3d  %(message)s",
    level_styles=log_styles,
    field_styles=field_styles,
    datefmt="%H:%M:%S",
)
# ls.set_format(fmt=f"[%({ls.fields.name})s] %({ls.fields.thread})-7s %({ls.fields.asctime})s %({ls.fields.module})-12s %({ls.fields.lineno})-3d  %({ls.fields.message})s")

logger.propagate = False  # prevents logs to pass to the root logger (needs to be after coloredlogs.install)
logger.setLevel(level=logging.DEBUG)
