FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r -g 1000 appuser && useradd -r -u 1000 -g appuser appuser

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Patch Streamlit's index.html to add PWA meta tags
RUN STREAMLIT_PATH=$(python -c "import streamlit; print(streamlit.__path__[0])") && \
    INDEX_FILE="$STREAMLIT_PATH/static/index.html" && \
    sed -i 's|<link rel="shortcut icon" href="./favicon.png" />|<link rel="shortcut icon" href="./favicon.png" />\n    <link rel="apple-touch-icon" sizes="180x180" href="/app/static/apple-touch-icon.png" />\n    <link rel="manifest" href="/app/static/manifest.json" />\n    <meta name="apple-mobile-web-app-capable" content="yes" />\n    <meta name="apple-mobile-web-app-title" content="CarWorth" />\n    <meta name="theme-color" content="#4A9EFF" />|' "$INDEX_FILE"

# Copy application code
COPY app/ ./app/
COPY .streamlit/ ./.streamlit/

# Set ownership and permissions
RUN chown -R appuser:appuser /app

# Create streamlit config directory for the user
RUN mkdir -p /home/appuser/.streamlit && chown -R appuser:appuser /home/appuser

# Switch to non-root user
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--browser.gatherUsageStats=false"]
