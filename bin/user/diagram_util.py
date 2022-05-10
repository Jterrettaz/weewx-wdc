import datetime
from calendar import monthrange, isleap
from weewx.cheetahgenerator import SearchList
from user.general_util import GeneralUtil


class DiagramUtil(SearchList):
    def get_diagram_type(self, observation):
        """
        Set e.g. "temp" for all diagrams which should be rendered as temp
        diagram (includes also heat anmd windchill).

        Args:
            observation (string): The observation

        Returns:
            str: A diagram type string
        """
        if observation in GeneralUtil.temp_obs or 'temp' in observation.lower():
            return 'temp'

        if 'humidity' in observation.lower():
            return 'humidity'

        if observation == 'windSpeed' or observation == 'windGust':
            return 'wind'

        if observation == 'barometer':
            return 'pressure'

        return observation

    def get_diagram(self, observation):
        """
        Choose between line and bar.

        Args:
            observation (string): The observation

        Returns:
            str: A diagram string
        """
        if observation == 'rain' or observation == 'ET':
            return 'bar'

        return 'line'

    def get_aggregate_type(self, observation):
        """
        aggregate_type for observations series.
        @see https://github.com/weewx/weewx/wiki/Tags-for-series#syntax

        Args:
            observation (string): The observation

        Returns:
            string: aggregate_type
        """
        if observation == 'ET' or observation == 'rain':
            return 'sum'

        return 'avg'

    def get_aggregate_interval(self, observation, precision):
        """
        aggregate_interval for observations series.
        @see https://github.com/weewx/weewx/wiki/Tags-for-series#syntax

        Args:
            observation (string): The observation
            precision (string): Day, week, month, year

        Returns:
            int: aggregate_interval
        """
        if precision == 'day':
            if observation == 'ET' or observation == 'rain':
                return 3600  # 1 hour

            return 900  # 15 minutes

        if precision == 'week':
            if observation == 'ET' or observation == 'rain':
                return 3600 * 24  # 1 day

            return 900 * 8  # 2 hours

        if precision == 'month':
            if observation == 'ET' or observation == 'rain':
                return 3600 * 24  # 1 day

            return 900 * 24  # 6 hours

        if precision == 'year':
            if observation == 'ET' or observation == 'rain':
                return 3600 * 24  # 1 day

            return 900 * 48  # 12 hours

    def get_rounding(self, observation):
        """
        Rounding settings for observations.

        Args:
            observation (string): The observation

        Returns:
            int: A rounding
        """
        if observation == 'UV' or observation == 'cloudbase':
            return 0

        if observation == 'ET':
            return 2

        return 1

    def get_delta(self, observation, precision):
        """
        Get delta for $span($hour_delta=$delta) call.

        Args:
            observation (string): The observation
            precision (string): Day, week, month, year

        Returns:
            float: A delta
        """
        now = datetime.datetime.now()

        if precision == 'day':
            hour_delta = 24

        if precision == 'week':
            hour_delta = 24 * 7

        if precision == 'month':
            hour_delta = 24 * monthrange(now.year, now.month)[1]

        if precision == 'year':
            days = 366 if isleap(now.year) else 365
            hour_delta = 24 * days

        if observation == 'rain' or observation == 'ET':
            # @todo Use time of last record instead of now.minute
            return round(hour_delta + (now.minute / 60), 2)

        return hour_delta