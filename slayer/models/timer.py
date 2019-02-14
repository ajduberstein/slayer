import datetime


import pandas as pd


VALID_INPUT_TYPES = ['frame_id', 'epoch', 'iso8601', 'datetime']


class Timer(object):
    """
    Timer
    ~~~
    Configuration governing time controls.

    Specifying a single `time_field` in a `Slayer` object will allow plotting data through time. However,
    if you'd like more fine-grained control, you should use this `Timer` object to configure
    the speed the data is cycled through, to enable user interactions with the timer,
    determine the size of the time delta between animations, or to decide how the time text itself is presented.

    Acceptable inputs for time fields are ISO-8601 timestamps, integers, epoch times, or
    `datetime.datetime` objects.

    Attributes: min_time (float): Earliest time listed in the data, in seconds.
        max_time (float): Latest time listed in the data, in seconds.
        js_display_format (str): Display string using Moment.js. For examples, see https://momentjs.com/
        js_tz (str): Timezone for moment.js, if other than UTC.
        increment_unit (float): Number of seconds to increment the timer by on every tick
        controls (:obj:`list` of :obj:`str`): List of timer controls to render.
    """

    def __init__(
            self,
            input_type='frame_id',
            increment_by=1,
            tick_rate=0.5,
            controls=['pause', 'play', 'fast_forward', 'rewind'],
            js_display_format=None,
            js_tz=None,
            loop=True,
            cumulative=True,
            min_time=float('inf'),
            max_time=float('-inf')):
        """
        Arguments:
            input_type (str): One of 'frame_id', 'epoch', or 'iso8601'. If 'frame_id', any number if acceptable.
                If 'epoch', all time fields will be interpreted as epoch timestamps. If 'iso8601', timestamp inputs
                will be interpreted as ISO-8601 timestamps.
            increment_by (:obj:`str` or :obj:`pandas.Timedelta`): Increase in the timer, given
                by either a pandas.Timedelta object its date-string argument, as seen in
                https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.Timedelta.html
            tick_rate (float): Refresh rate of the data in seconds
            controls (:obj:`list` of :obj:`str`): List of timer controls to render.
            js_display_format (str): Display string using Moment.js. For examples, see https://momentjs.com/
            min_time (float): Earliest time listed in the data, in as a float. Calculated from data if not passed.
            max_time (float): Last time listed in the data, as a float. Calculated from data if not passed.
        """
        self.min_time = min_time
        self.max_time = max_time
        self.increment_unit = float(self._get_increment_by(increment_by))
        self.controls = list(controls)
        self.tick_rate = float(tick_rate)
        self.input_type = self._interpret_input_type(input_type)
        self.loop = bool(loop)
        self.js_display_format = js_display_format or self._suggest_display_format(self.input_type)

    def _suggest_display_format(self, input_type):
        if input_type in ('iso8601', 'datetime', 'epoch'):
            return 'YYYY-MM-DD HH:mm:SS'
        return ''

    def _interpret_input_type(self, input_type):
        if input_type not in VALID_INPUT_TYPES:
            raise TypeError('Invalid input_type')
        return input_type

    def _get_increment_by(self, increment_by):
        if isinstance(increment_by, str):
            return pd.Timedelta(increment_by).total_seconds()
        if isinstance(increment_by, int) or isinstance(increment_by, float):
            return increment_by
        elif isinstance(increment_by, pd.Timedelta):
            return increment_by
        raise TypeError('Argument for `increment_by` can by a str or pandas.Timedelta')

    def coerce_to_number(self, ts):
        """Takes a datetime and converts it to a number for time incrementing"""
        try:
            if self.input_type == 'iso8601':
                return pd.Timestamp(ts).value / 10. ** 9
            if isinstance(ts, (datetime.date, datetime.datetime)):
                return pd.Timestamp(ts).value / 10. ** 9
            return float(ts)
        except ValueError as e:
            raise type(e)(str(e) + '. Error processing %s' % ts)

    def fit_min_and_max(self, layer):
        """Sets min/max time from a Layer"""
        self.min_time = min(self.coerce_to_number(layer.min_time), self.min_time)
        self.max_time = max(self.coerce_to_number(layer.max_time), self.max_time)

    def get_min_time(self):
        return self.min_time

    def get_max_time(self):
        return self.max_time

    def is_enabled(self):
        """Verify that at least one layer has a time field, enabling a Timer to render.

        Used to prevent rendering if there is no time field.

        Returns:
            bool: Boolean indicating that at least one layer has a time field
        """
        enabled = self.min_time != float('inf') and self.max_time != float('-inf')
        return enabled
