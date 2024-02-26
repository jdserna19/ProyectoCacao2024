import datetime as dt
import os


class DataSubdirectoryCreator:
    DATA_ROOT_DIR_NAME = "data/"
    LOCAL_TIMEZONE = dt.timezone(dt.timedelta(hours=-5))
    DATE_TIME_FORMAT = "%d%m%Y%H%M%S"

    def __init__(self, number_of_lots):
        self.number_of_lots = number_of_lots

    def create_data_subdirectories(self, timestamp):
        """Creates the necessary subdirectories for the data according to the given timestamp."""
        utc_timestamp = self.utc_to_local(timestamp)
        main_data_subdir = "{}{}/".format(self.DATA_ROOT_DIR_NAME, utc_timestamp.strftime(self.DATE_TIME_FORMAT))
        data_subdirs = list()
        # Creates the subdirectories for lot data.
        for i in range(self.number_of_lots):
            lot_data_subdir = "{}lot_{}/".format(main_data_subdir, str(i + 1))
            os.makedirs(lot_data_subdir)
            data_subdirs.append(lot_data_subdir)
        # Creates the subdirectory for general data.
        general_data_subdir = "{}general_data/".format(main_data_subdir)
        os.makedirs(general_data_subdir)
        data_subdirs.append(general_data_subdir)
        # Returns the paths to the created subdirectories.
        return main_data_subdir, data_subdirs

    def utc_to_local(self, utc_timestamp):
        """Converts a timestamp from UTC timezone into local timezone."""
        return utc_timestamp.replace(tzinfo=dt.timezone.utc).astimezone(tz=self.LOCAL_TIMEZONE)

    def timestamp_to_string(self, timestamp):
        """Converts a timestamp into its string representation using the defined date time format."""
        return timestamp.strftime(self.DATE_TIME_FORMAT)
