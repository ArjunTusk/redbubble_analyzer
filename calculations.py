import os

import pandas as pd


class calculations:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.dataframe = pd.DataFrame()
        self.parse_folder_path()

    def get_dataFrame(self):
        return self.dataframe
    def parse_folder_path(self):
        # Get a list of all CSV files in the folder
        csv_files = [file for file in os.listdir(self.folder_path) if file.endswith('.csv')]

        # Initialize an empty list to store DataFrames
        dfs = []

        # Iterate through each CSV file and read it into a DataFrame
        for file in csv_files:
            file_path = os.path.join(self.folder_path, file)
            df = pd.read_csv(file_path)
            dfs.append(df)
        self.dataframe = pd.concat(dfs, ignore_index=True)
        self.dataframe['Order Date'] = pd.to_datetime(self.dataframe['Order Date'])
        # Extract month and year from the 'date' column and create a new column with it
        self.dataframe['month_year'] = self.dataframe['Order Date'].dt.strftime('%Y-%m')
        self.dataframe['month'] = self.dataframe['Order Date'].dt.strftime('%Y-%m')

    def parse_file(self, file_to_parse):
        data_frame = pd.read_csv(file_to_parse)
        self.dataframe.append(data_frame, ignore_index=True)

    def date_range_parse(self, start_date, end_date):
        filtered_df = self.dataframe[
            (self.dataframe['month_year'] >= start_date) & (self.dataframe['month_year'] <= end_date)]
        filtered_df = filtered_df.sort_values(by='month_year')
        return filtered_df

    def group_it(self, list_it):
        self.dataframe.groupby([list_it[0], list_it[1]])[list_it[2]].sum()
