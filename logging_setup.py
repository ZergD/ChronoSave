# logging_setup.py
from __future__ import annotations
import logging, sys
from logging.handlers import RotatingFileHandler

def setup_logging(
    level: str = "INFO",
    log_file: str | None = None,
    json_file: str | None = None,
) -> logging.Logger:
    """
    Human-readable console logs; optional rotating file; optional JSON audit file.
    Levels: DEBUG/INFO/WARNING/ERROR
    """
    logger = logging.getLogger("filesync")
    if logger.handlers:  # re-init safe
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console — short, friendly
    try:
        from rich.logging import RichHandler  # type: ignore
        console = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_level=True,
            show_time=False,
            show_path=False,
        )
        console.setFormatter(logging.Formatter("%(message)s"))
    except Exception:
        console = logging.StreamHandler(sys.stderr)
        console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logger.addHandler(console)

    # Rotating text file — detailed
    if log_file:
        fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ))
        logger.addHandler(fh)

    # Optional JSON audit file (machine-friendly)
    if json_file:
        try:
            from pythonjsonlogger import jsonlogger  # pip install python-json-logger
            jh = RotatingFileHandler(json_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
            jh.setLevel(logging.DEBUG)
            jh.setFormatter(jsonlogger.JsonFormatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d"
            ))
            logger.addHandler(jh)
        except Exception:
            logger.warning("JSON logging requested but python-json-logger not available.")

    return logger
