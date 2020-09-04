"""
"""
import pytest

from src import translate, CronParsingException


class TestCronTranslate(object):
    """
    """
    def test_translate(self):
        assert 'Every minute on Sunday' == translate('* * * * 0')
        assert 'Every minute on Sunday' == translate('* * * * 7')
        assert 'Every minute on January' == translate('* * * 1 *')
        assert 'Every minute on Sunday in January' == translate('* * * 1 0')
        assert 'Every minute on the 1st of every month' == translate('* * 1 * *')
        assert 'Every minute on Sundays on the 1st of every month' == translate('* * 1 * 0')
        assert 'Every minute on January the 1st' == translate('* * 1 1 *')
        assert 'Every minute on Sundays on January the 1st' == translate('* * 1 1 0')
        assert 'Every minute at 12am' == translate('* 0 * * *')
        assert 'Every minute on Sundays at 12am' == translate('* 0 * * 0')
        assert 'Every minute on January at 12am' == translate('* 0 * 1 *')
        assert 'Every minute on Sundays on January at 12am' == translate('* 0 * 1 0')
        assert 'Every minute on the 1st of every month at 12am' == translate('* 0 1 * *')
        assert 'Every minute on Sundays on the 1st of every month at 12am' == translate('* 0 1 * 0')
        assert 'Every minute on January the 1st at 12am' == translate('* 0 1 1 *')
        assert 'Every minute on Sundays on January the 1st at 12am' == translate('* 0 1 1 0')
        assert 'Once an hour' == translate('0 * * * *')
        assert 'Once an hour on Sundays' == translate('0 * * * 0')
        assert 'Once an hour on January' == translate('0 * * 1 *')
        assert 'Once an hour on Sundays on January' == translate('0 * * 1 0')
        assert 'Once an hour on the 1st of every month' == translate('0 * 1 * *')
        assert 'Once an hour on Sundays on the 1st of every month' == translate('0 * 1 * 0')
        assert 'Once an hour on January the 1st' == translate('0 * 1 1 *')
        assert 'Once an hour on Sundays on January the 1st' == translate('0 * 1 1 0')
        assert 'Every day at 12:00am' == translate('0 0 * * *')
        assert 'Every Sunday at 12:00am' == translate('0 0 * * 0')
        assert 'Every day on January at 12:00am' == translate('0 0 * 1 *')
        assert 'Every Sunday on January at 12:00am' == translate('0 0 * 1 0')
        assert 'The 1st of every month at 12:00am' == translate('0 0 1 * *')
        assert 'The 1st of every month on Sundays at 12:00am' == translate('0 0 1 * 0')
        assert 'Every year on January the 1st at 12:00am' == translate('0 0 1 1 *')
        assert 'On Sundays on January the 1st at 12:00am' == translate('0 0 1 1 0')

        assert 'Every year on January the 1st at 12:00pm' == translate('0 12 1 1 *')
        assert 'Every minute on Mondays at 3pm' == translate('* 15 * * 1')
        assert 'Every minute on January the 3rd' == translate('* * 3 1 *')
        assert 'Every minute on Mondays on April' == translate('* * * 4 1')
        assert 'On Mondays on April the 22nd at 3:10pm' == translate('10 15 22 4 1')

        assert 'Every day at 10:00pm' == translate('0 22 * * *')
        assert 'Every day at 9:00am' == translate('0 9 * * *')
        assert 'Every Monday at 4:00pm' == translate('0 16 * * 1')
        assert 'Every year on January the 1st at 12:00am' == translate('0 0 1 1 *')
        assert 'The 1st of every month at 12:00am' == translate('0 0 1 * *')

    def test_extended_cron_syntax(self):
        assert 'Once an hour' == translate('@hourly')
        assert 'Every day at 12:00am' == translate('@daily')
        assert 'Every Sunday at 12:00am' == translate('@weekly')
        assert 'The 1st of every month at 12:00am' == translate('@monthly')
        assert 'Every year on January the 1st at 12:00am' == translate('@yearly')
        assert 'Every year on January the 1st at 12:00am' == translate('@annually')

    def test_one_into_once(self):
        assert 'Every minute at 8am' == translate('* 8-8 * * *')
        assert 'Every minute on January' == translate('* * * 1-1 *')

    def test_junctions_combinations(self):
        assert 'Every minute of every 2 hours' == translate('* */2 * * *')
        assert 'Every minute of every 3 hours on the 2nd of every month' == translate('* 1/3 2 * *')

    def test_expressions_increment(self):
        assert 'Every 2 minutes' == translate('*/2 * * * *')
        assert 'Every 2 minutes' == translate('1/2 * * * *')
        assert 'Twice every 4 minutes' == translate('1,3/4 * * * *')
        assert '3 times every 5 minutes' == translate('1-3/5 * * * *')
        assert 'Every 2 minutes at 2pm' == translate('*/2 14 * * *')
        assert 'Once an hour every 2 days' == translate('0 * */2 * *')
        assert 'Every minute every 2 days' == translate('* * */2 * *')
        assert 'Once every 2 hours' == translate('0 */2 * * *')
        assert 'Twice every 5 hours' == translate('0 1,2/5 * * *')
        assert 'Every minute 2 hours out of 5' == translate('* 1,2/5 * * *')
        assert 'Every day every 4 months at 12:00am' == translate('0 0 * */4 *')

    def test_expressions__multiple(self):
        assert 'Every minute 2 hours a day' == translate('* 8,18 * * *')
        assert 'Every minute 3 hours a day' == translate('* 8,18,20 * * *')
        assert 'Every minute 20 hours a day' == translate('* 1-20 * * *')
        assert 'Twice an hour' == translate('0,30 * * * *')
        assert 'Twice an hour 5 hours a day' == translate('0,30 1-5 * * *')
        assert '5 times a day' == translate('0 1-5 * * *')
        assert 'Every minute 5 hours a day' == translate('* 1-5 * * *')
        assert '5 days a month at 1:00am' == translate('0 1 1-5 * *')
        assert '5 days a month 2 months a year at 1:00am' == translate('0 1 1-5 5,6 *')
        assert '2 months a year on the 5th at 1:00am' == translate('0 1 5 5,6 *')
        assert 'The 5th of every month 4 days a week at 1:00am' == translate('0 1 5 * 1-4')

    def test_parsing_exception(self):
        with pytest.raises(CronParsingException):
            translate('INVALID_EXPRESSION')
            translate('P * * * *')
            translate('1,2-3 * * * *')
            translate('1/2/3 * * * *')
            translate('* * * 0 *')
            translate('* * * 13 *')
            translate('* * * * 8')

