import numpy as np

# Generate Walsh matrix of size n x n
def walsh_matrix(n):
    if n == 1:
        return np.array([[1]])
    else:
        H = walsh_matrix(n // 2)
        return np.block([[H, H], [H, -H]])

# Encode data using Walsh code
def encode_data(station_data, walsh_code):
    # Convert binary data (0 to -1)
    station_data_bipolar = np.array([1 if bit == 1 else -1 for bit in station_data])
    return station_data_bipolar * walsh_code

# Simulate CDMA transmission (sum of encoded data)
def cdma_transmission(encoded_signals):
    return np.sum(encoded_signals, axis=0)

# Decode received signal using Walsh code
def decode_data(received_signal, walsh_code):
    # Perform dot product and divide by length of Walsh code to normalize
    return np.dot(received_signal, walsh_code) // len(walsh_code)

# Main CDMA simulation
def cdma_simulation(stations_data):
    n = len(stations_data)
    
    # Ensure n is a power of 2 for Walsh codes
    if np.log2(n) % 1 != 0:
        raise ValueError("Number of stations must be a power of 2.")
    
    # Generate Walsh codes for n stations
    walsh_codes = walsh_matrix(n)
    print("Walsh matrix:",walsh_codes)
    
    # Encode data for each station
    encoded_signals = [encode_data(station_data, walsh_codes[i]) for i, station_data in enumerate(stations_data)]
    for i,encoded_signal in enumerate(encoded_signals):
        print(f"Station {i+1} encoded signal:",encoded_signal)
    
    # Transmit the encoded signals (sum them up)
    received_signal = cdma_transmission(encoded_signals)
    
    # Decode the data for each station
    decoded_data = [decode_data(received_signal, walsh_codes[i]) for i in range(n)]
    
    return decoded_data

# Example usage
if __name__ == "__main__":
    # Sample binary data from 4 stations (1 and 0 represent binary data)
    stations_data = [
        [1],  # Data from station 1
        [0],  # Data from station 2
        [1],  # Data from station 3
        [0],  # Data from station 4     
    ]
    
    print("Original Data from Stations:")
    for i, data in enumerate(stations_data):
        print(f"Station {i+1}: {data}")
    
    # Run CDMA simulation
    decoded_data = cdma_simulation(stations_data)
    
    print("\nDecoded Data at Receiver:")
    for i, data in enumerate(decoded_data):
        # Convert bipolar data back to binary (rounding first)
        decoded_binary = [1 if bit > 0 else 0 for bit in np.atleast_1d(data)]  # np.atleast_1d to ensure it's iterable
        print(f"Station {i+1}: {decoded_binary}")


