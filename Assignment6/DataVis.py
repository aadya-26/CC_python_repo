# Import the matplotlib library
import matplotlib.pyplot as plt

# Define the companies and their market influence
companies = ['The Fabricant', 'DressX', 'Replicant', 'RTFKT Studios', 'Carlings', 'Others']
influence = [25, 20, 15, 15, 10, 15]  # Hypothetical influence percentages

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(influence, labels=companies, autopct='%1.1f%%', startangle=140)

# Add a title
plt.title('Illustrative Influence Distribution in the Digital Fashion Industry')

# Show the chart
plt.show()
