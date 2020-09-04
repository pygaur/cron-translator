from .translator import Translate
from .exception import CronParsingException


def translate(cron):
    """
    :param cron:
    :return:
    """
    return Translate.translate(cron)
