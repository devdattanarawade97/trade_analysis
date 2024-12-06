import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import datetime

# Step 1: Fetch BTC data
symbol = "BTC-USD"
data = yf.download(symbol, start="2010-01-01")

# Prepare the data
prices = data['Close'].values.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(prices)

# Step 2: Create input-output pairs
sequence_length = 90  # Use the past 30 days to predict the next day
X, y = [], []
for i in range(len(scaled_prices) - sequence_length):
    X.append(scaled_prices[i:i + sequence_length])
    y.append(scaled_prices[i + sequence_length])
X, y = np.array(X), np.array(y)

# Step 3: Split the data into training and testing sets
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Step 4: Build the ANN (LSTM)
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    LSTM(50, return_sequences=False),
    Dense(25),
    Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))

# Step 5: Predict future prices
def predict_future(model, data, scaler, sequence_length, future_days):
    # Start with the last available sequence
    last_sequence = data[-sequence_length:].reshape(1, sequence_length, 1)
    future_predictions = []
    
    for _ in range(future_days):
        # Predict the next day
        next_prediction = model.predict(last_sequence)
        
        # Reshape next_prediction to be compatible with the sequence shape
        next_prediction = next_prediction.reshape(1, 1, 1)  # Shape should be (1, 1, 1)
        future_predictions.append(next_prediction[0, 0, 0])
        
        # Update the sequence with the predicted value (reshape to match the input shape)
        next_sequence = np.append(last_sequence[:, 1:, :], next_prediction, axis=1)
        last_sequence = next_sequence
    
    # Transform predictions back to original scale
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
    return future_predictions

# Define the number of future days to predict (until April 2025)
future_days = (datetime.date(2025,3, 1) - data.index[-1].date()).days


# Predict future prices
future_predictions = predict_future(model, scaled_prices, scaler, sequence_length, future_days)

# Log the first 10 future predicted values in the console
print("Future Predicted BTC Prices (for the first 10 days):")
for i in range(min(10, future_days)):
    print(f"Day {i+1}: {future_predictions[i][0]} USD")

# Create a future date range
future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=future_days)

# Combine future dates and predictions into a DataFrame
future_data = pd.DataFrame({'Date': future_dates, 'Predicted_Price': future_predictions.flatten()})
future_data.set_index('Date', inplace=True)

# Step 6: Plotting
plt.figure(figsize=(14, 7))

# Plot actual BTC prices starting from the point where the test predictions begin
plt.plot(data.index[split:], data['Close'][split:], label="Actual BTC Price (from Test Start)", color='blue')  # Actual BTC price from test start

# Plot test data predictions (predictions on test set)
test_predictions = model.predict(X_test)
test_predictions = scaler.inverse_transform(test_predictions)

# Ensure the date range matches the length of the test predictions
test_dates = data.index[split + sequence_length:split + sequence_length + len(test_predictions)]

plt.plot(test_dates, test_predictions, label="Test Data Predictions", color='orange')

# Plot future predictions
plt.plot(future_data.index, future_data['Predicted_Price'], label="Future Predictions (April 2025)", linestyle='--', color='green')

plt.title("BTC Price Prediction Until April 2025 Using ANN")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()
