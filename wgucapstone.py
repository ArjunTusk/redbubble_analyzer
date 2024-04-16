import os
import random

import pandas as pd
import shutil
from matplotlib import pyplot as plt, colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression


# filters out outliers
def filter_out(extracted_rows, axis_list):
    for i in axis_list:
        outliers = extracted_rows[
            (extracted_rows[i] - extracted_rows[i].mean()).abs() > 0.5 * extracted_rows[i].std()]
        extracted_rows = extracted_rows[~extracted_rows.index.isin(outliers.index)]
    return extracted_rows


# determines optimal price
def profit_maximization(price, data):
    quantity_sold = data['Quantity'].sum()  # Total quantity sold
    total_revenue = price * quantity_sold  # Total revenue
    total_cost = (data['Cost'] * data['Quantity']).sum()  # Total cost
    return total_revenue - total_cost


class calculations:
    def __init__(self, folder_path):
        final_path1 = os.getcwd()
        folder_path1 = os.path.join(final_path1, folder_path)
        self.folder_path = folder_path1
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
        absolute_folder_path = self.folder_path
        csv_files = os.listdir(absolute_folder_path)

        # Iterate through each CSV file and read it into a DataFrame
        for file in csv_files:
            file_path = os.path.join(absolute_folder_path, file)
            self.parse_file(file_path)
        self.dataframe['Order Date'] = pd.to_datetime(self.dataframe['Order Date'])
        # Extract month and year from the 'date' column and create a new column with it
        self.dataframe['month_year'] = self.dataframe['Order Date'].dt.strftime('%y-%m')
        self.dataframe['year'] = self.dataframe['Order Date'].dt.strftime('%y')
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
        destination_folder = self.folder_path
        # Check if the file exists
        if os.path.exists(file_path):
            # Move the file to the destination folder
            self.parse_file(file_path)
            shutil.move(file_path, destination_folder)
            print("File moved successfully!")
        else:
            print("File does not exist.")

    # splits the data frame so that it only includes dates between start_date and end_date
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

    # determines best product for the season
    def best_prod_for_season(self, months, y_axis):
        options22 = {"Jan - March": [1, 3], "April - June": [4, 6], "Jul - Sep": [7, 9], "Oct - Dec": [10, 12]}
        my_dict = {}
        e = self.date_range_parse(options22[months][0], options22[months][1], 'month')
        resulte = e.groupby('Product').agg({'Quantity': 'sum'}).reset_index()
        resulte = resulte[resulte["Quantity"] > 4]
        for o in resulte["Product"]:
            ret_price = self.optimal_price("Price", y_axis, o)
            if ret_price != -1:
                my_dict[o] = ret_price
        return my_dict

    def linear_reg(self, fig, product_sell, y_axis):
        # Step 3: Prepare your data
        extracted_rows = self.dataframe[self.dataframe['Product'] == product_sell]
        extracted_rows = extracted_rows.reset_index()
        result = extracted_rows.groupby('Price').agg({'Profit': 'median', 'Quantity': 'sum'}).reset_index()
        if extracted_rows['Profit'].min() >= 1:
            extracted_rows = filter_out(extracted_rows, {'Price', y_axis})
        else:
            extracted_rows = filter_out(extracted_rows, {'Quantity'})
            result = extracted_rows.groupby('Price').agg(
                {'Profit': 'median', 'Quantity': 'sum'}).reset_index()
        result['sum'] = result['Profit'] * result['Quantity']
        if result.shape[0] < 3:
            if y_axis == 'Profit':
                y_axis = 'sum'
            return -1
        # Extracting columns for linear regression
        X = result[['Price']]  # Feature
        y = result[y_axis]  # Target
        # Creating and fitting the linear regression model
        model = LinearRegression()
        model.fit(X, y)
        # Predicting Y values
        y_pred = model.predict(X)
        plot1 = fig.add_subplot(111)
        # Plotting the data points and the regression line
        plot1.scatter(X, y, color='blue', label='Actual Data')
        plot1.plot(X, y_pred, color='red', label='Linear Regression')
        plot1.set_xlabel('Retail Price')
        plot1.set_ylabel(y_axis)
        plot1.set_title('Linear Regression Model')
        return plot1

    # creates bar chart
    def bar_chart(self, frame_plots):
        fig, ax = plt.subplots()
        ax.bar(self.dataframe['year'], self.dataframe['Profit'])
        ax.set_xlabel('Year')
        ax.set_ylabel('Profit')
        ax.set_title('Bar Chart of Sales YoY')
        canvas = FigureCanvasTkAgg(fig, master=frame_plots)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

    # creates pie chart
    def pie_chatrt(self, frame_plots):
        fig, ax = plt.subplots()
        result = self.dataframe.groupby('Product').agg(
            {'Profit': 'sum', 'Quantity': 'sum'}).reset_index()
        year_cnt = self.dataframe.groupby('year').agg(
            {'Profit': 'sum', 'Quantity': 'sum'}).reset_index()
        min_amnt = 210
        result = result[result["Profit"] >= min_amnt]
        ax.pie(result['Profit'], labels=result['Product'], autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        title = 'Products that have >' + str(min_amnt) + ' over the last ' + str(len(year_cnt["year"])) + ' years'
        ax.set_title(title)
        canvas = FigureCanvasTkAgg(fig, master=frame_plots)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

    # redundant linear regression
    def linear_reg1(self, product_sell, y_axis):
        aa = self.date_range_parse(1, 3, "month")
        gg = aa
        list_it = []
        models = []
        X = gg[['month']]
        names = list(colors.cnames)
        for i in product_sell.keys():
            list_it.append(i)

        for a in range(len(list_it)):
            result = aa[aa['Product'] == list_it[a]]
            result = result.groupby('month').agg(
                {'Profit': 'median', 'Quantity': 'sum'}).reset_index()
            print(result)
            X = result[['month']]  # Feature
            y = result[y_axis]
            model = LinearRegression()
            model.fit(X, y)
            models.append(model)

        for a, model in enumerate(models):
            plt.plot(X, model.predict(X), color=random.choice(names))
        plt.show()
