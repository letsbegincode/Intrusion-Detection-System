# Network Intrusion Detection System

A Flask-based API for real-time network intrusion detection that works with Node.js packet captures.

## Overview

This system detects potential network attacks by analyzing packet timing patterns:

1. Node.js captures and formats network packets
2. Node.js sends packet data to Flask API
3. Flask extracts 12 time-based features 
4. Machine learning model predicts if the traffic pattern is an attack
5. API returns prediction results to Node.js

## Features Analyzed

The system extracts these timing-based features:
- Forward/Backward/Flow Inter-Arrival Time statistics (std, mean, max, total)
- Flow Duration
- Idle Time statistics

## Setup Instructions

### Prerequisites
- Python 3.8+
- Flask
- NumPy
- pandas
- scikit-learn ( LightGBM )
- Pickle

### Installation


2. Install requirements:
```
pip install -r requirements.txt
```

3. Add your trained model file (model.pkl) to the app directory

4. Run the application:
```
python run.py
```

## API Usage

Send POST requests to `/predict` with an array of packet objects:

```json
[
  {
    "timestamp": "2025-03-19T15:43:22.123456",
    "src_ip": "192.168.1.100",
    "dst_ip": "172.16.0.5",
    "src_port": 54321,
    "dst_port": 80
  },
  {
    "timestamp": "2025-03-19T15:43:22.234567",
    "src_ip": "172.16.0.5",
    "dst_ip": "192.168.1.100",
    "src_port": 80,
    "dst_port": 54321
  }
]
```

Response format:
```json
{
  "prediction": 1,       
  "is_attack": true     
}
```
Where:
- `prediction`: 0 for normal traffic, 1 for attack
- `is_attack`: Boolean flag for easy use in conditions

## Configuration

Adjust parameters in `config.py`:
- `IDLE_THRESHOLD`: Time in microseconds to consider a gap as idle (default: 1,000,000 μs / 1 second)
- `PREDICTION_THRESHOLD`: Probability threshold to classify as attack (default: 0.5)
