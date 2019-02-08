import pandas as pd


class Timer(object):
    """
    Timer
    ~~~
    Configuration governing time controls

    Attributes:
        min_time (float): Earliest time listed in the data, in seconds.
        max_time (float): Latest time listed in the data, in seconds.
        display_format (str): Moment.js string representation of the time format, see https://momentjs.com/
        increment_unit (float): Number of seconds to increment the timer by on every tick
        controls (:obj:`list` of :obj:`str`): List of timer controls to render.
        enable (bool): Should enable time controls
    """

    def __init__(
            self,
            increment_by='1 day',
            tick_rate=0.5,
            controls=['pause', 'play', 'fast_forward', 'rewind'],
            display_format='MMMM DD, YYYY',
            min_time=float('inf'),
            enable=True,
            max_time=float('-inf')):
        """
        Arguments:
            increment_by (:obj:`str` or :obj:`pandas.Timedelta`): Increase in the timer, given
                by either a pandas.Timedelta object its date-string argument, as seen in
                https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.Timedelta.html
            tick_rate (float): Refresh rate of the data in seconds
            controls (:obj:`list` of :obj:`str`): List of timer controls to render.
            display_format (str): Display string using Moment.js. For examples, see https://momentjs.com/
            min_time (float): Earliest time listed in the data, in seconds. Calculated from data if not passed.
            max_time (float): Last time listed in the data, in seconds. Calculated from data if not passed.
        """
        self.min_time = self.min_time
        self.max_time = self.max_time
        self.display_format = str(display_format)
        self.increment_unit = float(self._get_increment_by(increment_by).total_seconds())
        self.controls = list(controls)
        self.tick_rate = float(tick_rate)

    def _get_increment_by(self, increment_by):
        if isinstance(increment_by, str):
            return pd.Timedelta(increment_by)
        elif isinstance(increment_by, pd.Timedelta):
            return increment_by
        raise TypeError('Argument for `increment_unit` can by a str or pandas.Timedelta')

    def convert_ts_to_seconds(self, datetime_item):
        return pd.Timestamp(datetime_item).total_seconds()

    def adapt_to_layer(self, layer):
        """Enables Timer if layer is present and sets min/max time from a layer"""
        self.enable = layer.time_field or self.enable
        self.min_time = min(layer.min_time, self.min_time)
        self.max_time = max(layer.max_time, self.max_time)
