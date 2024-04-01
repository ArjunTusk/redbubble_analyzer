import pandas as pd
import matplotlib.pyplot as plt
import calculations as cal

# Sample DataFrame with sales data
lala = cal.calculations("C:/Users/Pam/IdeaProjects/capstone/csvs to load")
df = lala.get_dataFrame()


# Group by 'Product' and 'Month', then calculate the total quantity sold
monthly_sales = df.groupby(['Product', 'month_year'])['Quantity'].sum()

print(monthly_sales)


# Plotting
plt.figure(figsize=(20, 12))  # Adjust figure size if needed

# Iterate over each product
for product in df['Product'].unique():
    product_data = monthly_sales[product]  # Extract data for the product
    plt.plot(product_data.index, product_data.values, label=product)

# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Quantity Sold')
plt.title('Monthly Sales of Products')

# Adding legend
plt.legend()

# Show plot
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent labels from being cut off
plt.show()
