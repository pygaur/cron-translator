from .translator import Translate
from .exception import CronParsingException  # noqa: F401


def translate(cron):
    """
    :param cron:
    :return:
    """
    return Translate.translate(cron)
