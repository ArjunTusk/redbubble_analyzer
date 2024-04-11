import os

import numpy as np
import pandas as pd
import shutil
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression


def filter_out(extracted_rows, axis_list):
    for i in axis_list:
        outliers = extracted_rows[
            (extracted_rows[i] - extracted_rows[i].mean()).abs() > 0.5 * extracted_rows[i].std()]
        extracted_rows = extracted_rows[~extracted_rows.index.isin(outliers.index)]
    return extracted_rows


def profit_maximization(price, data):
    quantity_sold = data['Quantity'].sum()  # Total quantity sold
    total_revenue = price * quantity_sold  # Total revenue
    total_cost = (data['Cost'] * data['Quantity']).sum()  # Total cost
    return total_revenue - total_cost


class calculations:
    def __init__(self, folder_path):
        self.counter = 0
        self.folder_path = folder_path
        self.dataframe = pd.DataFrame()
        self.parse_folder_path()
        self.dataframe['Retail Price (USD)'] = self.dataframe['Retail Price (USD)'] / self.dataframe['Quantity']
        self.dataframe['Manufacturing Price (USD)'] = self.dataframe['Manufacturing Price (USD)'] / self.dataframe[
            'Quantity']
        self.dataframe['Artist Margin (USD)'] = self.dataframe['Artist Margin (USD)'] / self.dataframe[
            'Quantity']
        self.dataframe = self.dataframe.rename(columns={'Retail Price (USD)': 'Price'})
        self.dataframe = self.dataframe.rename(columns={'Manufacturing Price (USD)': 'Cost'})
        self.dataframe = self.dataframe.rename(columns={'Artist Margin (USD)': 'Profit'})
        columns_to_round = ['Price', 'Cost']
        self.dataframe[columns_to_round] = self.dataframe[columns_to_round].round(0)
        columns_to = ['Profit']
        self.dataframe[columns_to] = self.dataframe[columns_to].round(2)

    # returns the data frame
    def get_dataframe(self):
        return self.dataframe

    # gets the csv files from a folder
    def parse_folder_path(self):
        # Get a list of all CSV files in the folder
        absolute_folder_path = os.path.abspath(self.folder_path)
        csv_files = os.listdir(absolute_folder_path)

        # Iterate through each CSV file and read it into a DataFrame
        for file in csv_files:
            file_path = os.path.join(absolute_folder_path, file)
            self.parse_file(file_path)
        self.dataframe['Order Date'] = pd.to_datetime(self.dataframe['Order Date'])
        # Extract month and year from the 'date' column and create a new column with it
        self.dataframe['month_year'] = self.dataframe['Order Date'].dt.strftime('%y-%m')
        self.dataframe['month'] = self.dataframe['Order Date'].dt.strftime('%m').astype(int)
        self.dataframe = self.dataframe.sort_values(by='month_year').reset_index()

    # parse files and appends it to the current data frame
    def parse_file(self, file_to_parse):
        if file_to_parse.endswith('.csv'):  # Assuming you have CSV files
            dfs = pd.read_csv(file_to_parse)
            if self.dataframe.empty:
                self.dataframe = dfs
            else:
                self.dataframe = pd.concat([self.dataframe, dfs], ignore_index=True)

    # calls parse file to append to data frame. Moves file to destination folder.
    def add_file(self, file_path):
        # Define paths to the file and destination folder
        # Replace this with the path to your file
        destination_folder = 'C:/Users/Pam/IdeaProjects/capstone/csvs to load'
        # Check if the file exists
        if os.path.exists(file_path):
            # Move the file to the destination folder
            self.parse_file(file_path)
            shutil.move(file_path, destination_folder)
            print("File moved successfully!")
        else:
            print("File does not exist.")

    def date_range_parse(self, start_date, end_date, column_name):
        filtered_df = self.dataframe[
            (self.dataframe[column_name] >= start_date) & (self.dataframe[column_name] <= end_date)]
        filtered_df = filtered_df.sort_values(by=column_name)
        return filtered_df

    # Creates a simple linear regressions
    def optimal_price(self, x_axis, y_axis, product_sell):
        extracted_rows = self.dataframe[self.dataframe['Product'] == product_sell]
        extracted_rows = extracted_rows.reset_index()

        if extracted_rows['Profit'].min() >= 1:
            extracted_rows = filter_out(extracted_rows, {x_axis, y_axis})
        else:
            extracted_rows = filter_out(extracted_rows, {'Quantity'})
        result = extracted_rows.groupby('Price').agg(
            {'Profit': 'median', 'Quantity': 'sum', 'Cost': 'median'}).reset_index()
        result['sum'] = result['Profit'] * result['Quantity']
        if result.shape[0] < 3:
            if y_axis == 'Profit':
                y_axis = 'sum'
            return -1
        return result.loc[result[y_axis] == result[y_axis].max(), 'Price'].values[0]
        # Creates a simple linear regressions

    def best_prod_for_season(self, start_month, end_month, y_axis):
        lada = self.get_dataframe()['Product'].unique()
        a = lada.tolist()
        my_dict = {}
        i = start_month
        e = self.date_range_parse(start_month, end_month, 'month')
        resulte = e.groupby('Product').agg({'Quantity': 'sum'}).reset_index()
        resulte = resulte[resulte["Quantity"] > 4]
        for o in resulte["Product"]:
            ret_price = self.optimal_price("Price", y_axis, o)
            if ret_price != -1:
                my_dict[o] = ret_price
        return my_dict

    def linear_reg(self):
        # Step 2: Load your data
        # Assuming you have a DataFrame named 'df' with columns 'X_column' and 'y_column'
        # Replace 'X_column' and 'y_column' with the actual column names in your DataFrame
        # Example: df = pd.read_csv('your_dataset.csv')
        # Example: X_column = df['X_column']
        # Example: y_column = df['y_column']

        # Step 3: Prepare your data
        extracted_rows = self.dataframe[self.dataframe['Product'] == 'Greeting Card']
        extracted_rows = extracted_rows.reset_index()
        result = extracted_rows.groupby('month').agg({'Profit': 'median', 'Quantity': 'sum'}).reset_index()
        # Extracting columns for linear regression
        X = result[['month']]  # Feature
        y = result['Quantity']  # Target
        # Creating and fitting the linear regression model
        model = LinearRegression()
        model.fit(X, y)
        # Predicting Y values
        y_pred = model.predict(X)

        # Plotting the data points and the regression line
        plt.scatter(X, y, color='blue', label='Actual Data')
        plt.plot(X, y_pred, color='red', label='Linear Regression')
        plt.xlabel('Month')
        plt.ylabel('Quantity')
        plt.title('Linear Regression Model')
        plt.legend()
        plt.show()
