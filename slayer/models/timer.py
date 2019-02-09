import pandas as pd


class Timer(object):
    """
    Timer
    ~~~
    Configuration governing time controls.

    Note that specifying a single time field in the Slayer object will allow playing data through time. However,
    if you'd like more fine-grained control, you should use this Timer object to configure
    the speed the data is cycled through, whether the UI displays code that enables user interaction
    with the timer, determines the size of the time delta between animations, or how the time is presented.

    Attributes:
        min_time (float): Earliest time listed in the data, in seconds.
        max_time (float): Latest time listed in the data, in seconds.
        display_format (str): Moment.js string representation of the time format, see https://momentjs.com/
        increment_unit (float): Number of seconds to increment the timer by on every tick
        controls (:obj:`list` of :obj:`str`): List of timer controls to render.
    """

    def __init__(
            self,
            increment_by=1,
            tick_rate=0.5,
            controls=['pause', 'play', 'fast_forward', 'rewind'],
            display_format=None,
            force_datetime=False,
            cumulative=True,
            min_time=float('inf'),
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
            force_datetime (bool): Forces the interpretation of the input times as date-times.
        """
        self.min_time = min_time
        self.max_time = max_time
        self.display_format = str(display_format) if display_format is not None else None
        self.increment_unit = float(self._get_increment_by(increment_by))
        self.controls = list(controls)
        self.tick_rate = float(tick_rate)
        self.force_datetime = bool(force_datetime)

    def _get_increment_by(self, increment_by):
        if isinstance(increment_by, str):
            return pd.Timedelta(increment_by).total_seconds()
        if isinstance(increment_by, int) or isinstance(increment_by, float):
            return increment_by
        elif isinstance(increment_by, pd.Timedelta):
            return increment_by
        raise TypeError('Argument for `increment_by` can by a str or pandas.Timedelta')

    def coerce_to_number(self, datetime_item):
        """Takes a datetime and converts it to a number for time incrementing"""
        if self.force_datetime is True:
            return pd.Timestamp(datetime_item).value / 10. ** 9
        elif isinstance(datetime_item, float) or isinstance(datetime_item, int):
            return datetime_item
        return pd.Timestamp(datetime_item).value / 10. ** 9

    def fit_min_and_max(self, layer):
        """Enables Timer if layer is present and sets min/max time from a layer"""
        self.min_time = min(layer.min_time, self.min_time)
        self.max_time = max(layer.max_time, self.max_time)

    def is_enabled(self):
        """Verify that at least one layer has a time field, enabling a Timer to render.

        Used to prevent rendering if there is no time field.

        Returns:
            bool: Boolean indicating that at least one layer has a time field
        """
        return self.min_time != float('inf') and self.max_time != float('-inf')
