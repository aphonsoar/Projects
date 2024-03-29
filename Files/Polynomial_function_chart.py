#import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg')
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

spend = np.array([10, 20, 30, 40, 50])  # Example spend data
sales = np.array([50, 70, 90, 100, 95])  # Example sales data

# Polynomial function that represents the data 2nd-degree polynomial (quadratic function):
def polynomial_func(x, a, b, c):
    return a * x**2 + b * x + c # 2nd-degree polynomial function
# 3rd-degree polynomial
# def polynomial_func(x, a, b, c, d):
#     return a * x**3 + b * x**2 + c * x + d
# As the degree of the polynomial increases, the model can become more complex and may overfit the data.
# It's important to carefully consider the degree based on the complexity of the problem and the amount of available data to avoid overfitting.

# Fit the polynomial function to the data using curve fitting. This will estimate the coefficients of the polynomial that best fits the data:
coefficients, _ = curve_fit(polynomial_func, spend, sales)

# Generate a set of spend values for the polynomial forecast. You can use the linspace function from NumPy to create a range of spend values:
spend_forecast = np.linspace(spend.min(), spend.max(), 100)

# Use the estimated coefficients to calculate the forecasted sales based on the polynomial function:
sales_forecast = polynomial_func(spend_forecast, *coefficients)

# matplotlib
# plt.scatter(spend, sales, label='Actual Data')
# plt.plot(spend_forecast, sales_forecast, 'r-', label='Polynomial Forecast')
# plt.xlabel('Spend')
# plt.ylabel('Sales')
# plt.legend()
# plt.show()

# plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=spend, y=sales, mode='markers', name='Actual Data', marker=dict(size=10)))
fig.add_trace(go.Scatter(x=spend_forecast, y=sales_forecast, mode='lines', name='Polynomial Forecast', line=dict(width=3)))
fig.update_layout(title='Spend vs. Sales', xaxis_title='Spend', yaxis_title='Sales')
fig.show()
fig.write_html('C:\\Polynomial function chart.html')

optimal_spend = spend_forecast[np.argmax(sales_forecast)]
optimal_sales = np.max(sales_forecast)
print(f"Optimal Spend: {round(optimal_spend,2)}")
print(f"Forecasted Sales at Optimal Spend: {round(optimal_sales,2)}")
# Optimal Spend: 43.94
# Forecasted Sales at Optimal Spend: 97.97

# Calculate R-squared
r2 = r2_score(sales, polynomial_func(spend, *coefficients))
print(f"R-squared: {round(r2,4)}")
