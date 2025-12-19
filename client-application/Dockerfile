# Multi-stage build for Python 3.12 with Cython compilation
# Stage 1: Build the Cython extension
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy source files
COPY requirements.txt .
COPY setup.py .
COPY pyproject.toml .
COPY core/ ./core/
COPY models/ ./models/
COPY services/ ./services/
COPY controllers/ ./controllers/
COPY utils/ ./utils/

# Install Python dependencies and build Cython extension
RUN pip install --no-cache-dir cython setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py build_ext --inplace

# Stage 2: Create the runtime image
FROM python:3.12-slim

WORKDIR /app

# Install only runtime dependencies
COPY --from=builder /build/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the compiled extension and application files
COPY --from=builder /build/core/*.so ./core/
COPY --from=builder /build/core/__init__.py ./core/

# Copy Python source files (models, services, controllers, utils)
COPY models/ ./models/
COPY services/ ./services/
COPY controllers/ ./controllers/
COPY utils/ ./utils/
COPY main.py .

# Copy public key if it exists (optional - can be embedded in compiled module)
COPY pub.pe[m] ./

# License file will be mounted at runtime
# docker run -v /path/to/license.lic:/app/license.lic licensed-app:1.0

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from services.license_service import LicenseService; s = LicenseService(); s.validate_license()" || exit 1

# Default command
CMD ["python", "main.py"]
