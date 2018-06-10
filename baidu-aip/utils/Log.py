# -*- coding: utf-8 -*-
__author__='Kerwin zhang'
import os
import sys
import configparser
import logging
import logging.config
import warnings

LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


class LogConfig(object):
    def __init__(self, log_config_file, log_dir=None):
        self.log_config_file = log_config_file
        self.log_config = configparser.RawConfigParser()
        self.log_config.read(self.log_config_file)
        self.logger_prefix = "logger_"
        self.handler_prefix = "handler_"
        self.formatter_prefix = "formatter_"
        self.log_dir = log_dir

        self._check_section()
        self._parse_option()

    def _check_section(self):
        # check logger
        self.__check_logger()
        # check handler
        self.__check_handler()
        # check formatter
        self.__check_formatter()

    def _parse_option(self):
        # parse formatter option
        for formatter, formatter_info in self.formatters.items():
            section_name = formatter_info["section_name"]
            fmt = self.log_config.get(section_name, "format")
            datefmt = self.log_config.get(section_name, "datefmt")
            self.formatters[formatter]["value"] = logging.Formatter(fmt, datefmt)

        # parse handlers
        for handler, handler_info in self.handlers.items():
            section_name = handler_info["section_name"]
            handler_class = self.log_config.get(section_name, "class")
            handler_args = eval(self.log_config.get(section_name, "args"))
            handler_level = self.log_config.get(section_name, "level")
            handler_formatter = self.log_config.get(section_name, "formatter")
            _handler = eval("logging." + handler_class)
            if handler_class == 'FileHandler':
                if self.log_dir:
                    handler_args = list(handler_args)
                    handler_args[0] = os.path.join(self.log_dir, handler_args[0])
                else:
                    warnings.warn("logdir not defined, saving log file to current dir")
            self.handlers[handler]["value"] = _handler(*handler_args)
            self.handlers[handler]["value"].setLevel(LEVELS.get(handler_level.upper(), LEVELS["INFO"]))
            self.handlers[handler]["value"].setFormatter(self.formatters[handler_formatter]["value"])

        # parse logger
        for logger, logger_info in self.loggers.items():
            section_name = logger_info["section_name"]
            self.__parse_logger(logger, section_name)

    def __parse_logger(self, logger_name, section_name):
        tuple_items = self.log_config.items(section_name)
        logger = logging.getLogger(logger_name)
        for k, v in tuple_items:
            if k == "handlers":
                handlers = filter(None, [h.strip() for h in v.split(",")])
                for h in handlers:
                    logger.addHandler(self.handlers[h]["value"])
            if k == "level" and v:
                logger.setLevel(LEVELS.get(v, LEVELS["INFO"]))
            if k == "propagate" and v:
                logger.propagate = int(v)
        self.loggers[logger_name]["value"] = logger

    def __check_logger(self):
        _loggers = self.log_config.get("loggers", "keys").split(",")
        self.loggers = {}
        for logger in _loggers:
            logger = logger.strip()
            if logger:
                logger_section_name = self.logger_prefix + logger
                if not self.log_config.has_section(logger_section_name):
                    raise Exception("ERROR: No logger section name: %s" % logger_section_name)
                self.loggers.setdefault(logger, {})
                self.loggers[logger]["section_name"] = logger_section_name
        if not self.loggers:
            raise Exception("ERROR: No logger keys in %s" % self.log_config_file)

    def __check_handler(self):
        _handlers = self.log_config.get("handlers", "keys").split(",")
        self.handlers = {}
        for handler in _handlers:
            handler = handler.strip()
            if handler:
                handler_section_name = self.handler_prefix + handler
                if not self.log_config.has_section(handler_section_name):
                    raise Exception("ERROR: No handler section name: %s" % handler_section_name)
                self.handlers.setdefault(handler, {})
                self.handlers[handler]["section_name"] = handler_section_name
        if not self.handlers:
            raise Exception("ERROR: No handler keys in %s" % self.log_config_file)

    def __check_formatter(self):
        _formatters = self.log_config.get("formatters", "keys").split(",")
        self.formatters = {}
        for formatter in _formatters:
            formatter = formatter.strip()
            if formatter:
                formatter_section_name = self.formatter_prefix + formatter
                if not self.log_config.has_section(formatter_section_name):
                    raise Exception("ERROR: No formatter section name: %s" % formatter_section_name)
                self.formatters.setdefault(formatter, {})
                self.formatters[formatter]["section_name"] = formatter_section_name
        if not self.formatters:
            raise Exception("ERROR: No formatter keys in %s" % self.log_config_file)

    def get_logger(self, logger_name="root"):
        return self.loggers[logger_name]["value"]


from .Constants import ROOT_DIR, LOG_PATH

base_path = os.path.join(ROOT_DIR, "Housing")
utils_path = os.path.join(base_path, "utils")
log_config_file = os.path.join(utils_path, "logger.ini")

log_config = LogConfig(log_config_file, log_dir=LOG_PATH)
logger = log_config.get_logger('root')
drop_ship_po_process_logger = log_config.get_logger('drop_ship_po_process')
