import os
import json
import logging
import sys
from datetime import datetime
from logging import Handler, LogRecord
from common.config import config

# Custom log levels
NOTICE_LEVEL = 25
TRACE_LEVEL = 5

logging.addLevelName(NOTICE_LEVEL, "NOTICE")
logging.addLevelName(TRACE_LEVEL, "TRACE")

class GameLogHandler(Handler):
    """
    Custom handler to direct game-specific logs to their respective files.
    """
    def __init__(self, log_folder: str):
        super().__init__()
        self.log_folder = log_folder
        self.streams = {}

        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    def emit(self, record: LogRecord):
        try:
            game_category = getattr(record, "game_category", None)
            if not game_category:
                return

            if game_category not in self.streams:
                log_path = os.path.join(self.log_folder, f"{game_category}.log")
                self.streams[game_category] = open(log_path, "a", encoding="utf-8")

            stream = self.streams[game_category]
            msg = self.format(record)
            stream.write(f"{msg}\n")
            stream.flush()
        except Exception:
            self.handleError(record)

    def close(self):
        for stream in self.streams.values():
            stream.close()
        super().close()

class LogFormatter(logging.Formatter):
    """
    Formatter that defines console and file output style.
    """
    COLORS = {
        'DEBUG': 36,     # Cyan
        'INFO': 1,       # Default/White
        'WARNING': 33,  # Yellow
        'ERROR': 41,    # Red background
        'CRITICAL': 41, # Red background
        'NOTICE': 32,   # Green
        'TRACE': 35,    # Magenta
    }

    def __init__(self, use_color=False):
        super().__init__()
        self.use_color = use_color

    def format(self, record: LogRecord) -> str:
        date = datetime.fromtimestamp(record.created)
        level_name = record.levelname
        
        # Mapping level names for titles
        title = level_name
        if title == "WARNING":
            title = "WARNING"
        
        formatted_title = f"[{title}]"
        space = " " * max(9 - len(formatted_title), 0)

        # Handle data formatting (similar to _format_data)
        if isinstance(record.msg, (list, tuple)):
            parsed = [json.dumps(d) if isinstance(d, (dict, list)) else str(d) for d in record.msg]
            message = " ".join(parsed)
        else:
            message = record.msg

        if self.use_color:
            color = self.COLORS.get(level_name, 1)
            colored_title = f"\033[1m\033[37m\033[{color}m{formatted_title}\033[0m"
            return f"{date} {colored_title}{space} {message}"
        
        return f"[{date}] {formatted_title}{space} {message}"

class Log:
    def __init__(self):
        self.debugging = config.debugging
        self.logger = logging.getLogger(config.name)
        self.logger.setLevel(logging.DEBUG if self.debugging else logging.INFO)
        self.logger.propagate = False

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(LogFormatter(use_color=True))
        
        # Filter for console based on config.debug_level
        log_level_filter = config.debug_level or "all"
        if log_level_filter != "all":
            class LevelFilter(logging.Filter):
                def filter(self, record):
                    return record.levelname.lower() == log_level_filter.lower()
            console_handler.addFilter(LevelFilter())

        self.logger.addHandler(console_handler)

        # File Handlers
        if config.fs_debugging:
            runtime_handler = logging.FileHandler("runtime.log", encoding="utf-8")
            runtime_handler.setFormatter(LogFormatter(use_color=False))
            self.logger.addHandler(runtime_handler)

        self.logs_handler = logging.FileHandler("logs.log", encoding="utf-8")
        self.logs_handler.setFormatter(LogFormatter(use_color=False))
        # We only want 'log' calls to go here in the original, but let's see.
        # Actually in original Log.log() writes to logs.log.

        self.bugs_handler = logging.FileHandler("bugs.log", encoding="utf-8")
        self.bugs_handler.setFormatter(LogFormatter(use_color=False))

        # Game-specific handler
        self.game_handler = GameLogHandler("logs")
        self.game_handler.setFormatter(LogFormatter(use_color=False))
        self.logger.addHandler(self.game_handler)

    def _log(self, level, data, game_category=None, extra_handler=None):
        extra = {}
        if game_category:
            extra["game_category"] = game_category
        
        # We use a trick to pass multiple args as record.msg
        self.logger.log(level, data, extra=extra)
        
        if extra_handler:
            # Manually trigger extra handlers if they aren't attached to the main logger
            # or have special logic. In our case, bug() and log() are specific.
            record = self.logger.makeRecord(
                self.logger.name, level, "(unknown)", 0, data, None, None, None, extra
            )
            extra_handler.emit(record)

    def info(self, *data):
        self._log(logging.INFO, data)

    def debug(self, *data):
        if not self.debugging:
            return
        self._log(logging.DEBUG, data)

    def warning(self, *data):
        self._log(logging.WARNING, data)

    def error(self, *data):
        self._log(logging.ERROR, data)

    def critical(self, *data):
        self._log(logging.CRITICAL, data)

    def assert_log(self, assertion, *data):
        if assertion:
            return
        self._log(logging.ERROR, data)

    def notice(self, *data):
        self._log(NOTICE_LEVEL, data)

    def trace(self, *data):
        self._log(TRACE_LEVEL, data)

    def bug(self, *data):
        self.warning(*data)
        # BUGS are special, they go to bugs.log via extra_handler
        self._log(logging.WARNING, data, extra_handler=self.bugs_handler)

    def log(self, *data):
        # LOGS are special, they go to logs.log via extra_handler
        self._log(logging.INFO, data, extra_handler=self.logs_handler)

    # Game-specific loggers
    def chat(self, *data):
        self._log(logging.INFO, data, game_category="chat")

    def drop(self, *data):
        self._log(logging.INFO, data, game_category="drops")

    def general(self, *data):
        self._log(logging.INFO, data, game_category="general")

    def stores(self, *data):
        self._log(logging.INFO, data, game_category="stores")

    def trade(self, *data):
        self._log(logging.INFO, data, game_category="trades")

log = Log()
