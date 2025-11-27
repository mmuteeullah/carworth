# CarWorth

Used Car Value Calculator for India

## Features

- Calculate fair market value of any used car
- State-wise RTO tax calculation
- Brand-specific depreciation rates
- Ownership premium adjustments
- Mileage-based adjustments
- Condition assessments
- Deal verdict (Good Deal / Fair / Overpriced)
- Due diligence checklist

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app/main.py
```

### Docker

```bash
# Build and run
docker-compose up --build

# Or manually
docker build -t carworth .
docker run -p 8501:8501 carworth
```

Access at http://localhost:8501

## Project Structure

```
carworth/
├── app/
│   ├── main.py              # Streamlit entry point
│   ├── config.py            # Configuration
│   ├── calculators/         # Calculation logic
│   ├── data/                # Static data (taxes, brands)
│   ├── components/          # UI components
│   ├── utils/               # Utilities
│   └── assets/              # Logo, CSS
├── tests/                   # Unit tests
├── k8s/                     # Kubernetes manifests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## Deployment

### Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Configuration

Environment variables:
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Bind address (default: 0.0.0.0)

## License

MIT
