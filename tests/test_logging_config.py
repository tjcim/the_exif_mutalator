""" Test logging_config.py """
import logging

from context import logging_config  # pylint: disable=unused-import


def test_logging_level():
    """ Test that we start off at level 20 (INFO) """
    logger = logging.getLogger()
    assert logger.level == 20


def test_logging_formatter():
    """ Test that the formatter is working as expected. """
    logger = logging.getLogger()
    rec1 = logging.LogRecord('b', 50, 'b.tests', 3, 'this is the message', None, None)
    assert logger.handlers[0].format(rec1) == '[CRITICAL][b] this is the message'
    rec1 = logging.LogRecord('b', 40, 'b.tests', 3, 'this is the message', None, None)
    assert logger.handlers[0].format(rec1) == '[ERROR][b] this is the message'
    rec1 = logging.LogRecord('b', 30, 'b.tests', 3, 'this is the message', None, None)
    assert logger.handlers[0].format(rec1) == '[WARNING][b] this is the message'
    rec1 = logging.LogRecord('b', 20, 'b.tests', 3, 'this is the message', None, None)
    assert logger.handlers[0].format(rec1) == '[INFO][b] this is the message'
    rec1 = logging.LogRecord('b', 10, 'b.tests', 3, 'this is the message', None, None)
    assert logger.handlers[0].format(rec1) == '[DEBUG][b] this is the message'
