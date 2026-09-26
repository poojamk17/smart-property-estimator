
from predictor import predict

sample = [
    3.5,     # MedInc
    20.0,    # HouseAge
    5.0,     # AveRooms
    1.0,     # AveBedrms
    1000.0,  # Population
    3.0,     # AveOccup
    34.0,    # Latitude
    -120.0   # Longitude
]

result = predict(sample)

print("Prediction:", result)
print("Predicted value in dollars:", result * 100000)
