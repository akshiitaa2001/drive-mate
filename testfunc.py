import pandas as pd
from datetime import datetime

# Simulate Rental data for testing
data = pd.DataFrame({
    'Pickup_Date': [datetime(2024, 12, 1), datetime(2024, 12, 2), datetime(2024, 12, 3)],
    'Return_Date': [datetime(2024, 12, 5), datetime(2024, 12, 4), datetime(2024, 12, 6)]
})

# Calculate delays
data['Delay_Days'] = (data['Return_Date'] - data['Pickup_Date']).dt.days
print("Processed Data for Delays:", data)

# Count delays
delay_counts = data['Delay_Days'].value_counts().reset_index(name='Count').rename(columns={'index': 'Delay_Days'})
print("Delay Counts:", delay_counts)
