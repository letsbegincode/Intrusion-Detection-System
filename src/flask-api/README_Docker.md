## Docker Deployment

This application can be easily deployed using Docker. Here's how to get started:

### Prerequisites
- Docker
- Docker Compose

### Running with Docker Compose

1. Make sure your trained model file (`model.pkl`) is in the project root directory.

2. Build and start the containers:
```bash
docker-compose up -d
```

3. Check that the service is running:
```bash
curl http://localhost:5000/health
```

4. To stop the services:
```bash
docker-compose down
```

### Building and Running Manually

If you prefer to build and run the Docker container manually:

1. Build the Docker image:
```bash
docker build -t network-ids:latest .
```

2. Run the container:
```bash
docker run -p 5000:5000 -v $(pwd)/model.pkl:/app/app/models/model.pkl:ro network-ids:latest
```

### Environment Variables

The following environment variables can be set to configure the application:

- `MODEL_PATH`: Path to the trained model file (default: `app/models/model.pkl`)
- `IDLE_THRESHOLD`: Microseconds to consider a gap as idle (default: 1000000)
- `PREDICTION_THRESHOLD`: Probability threshold to classify as attack (default: 0.5)