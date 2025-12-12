# Cython-Based Licensing Solution POC

A complete offline licensing solution for Dockerized applications using Cython-compiled modules and RSA-signed licenses.

## Project Structure

```
Obfuscation-POC/
├── server-application/          # License generation server
│   ├── controllers/
│   │   └── license_controller.py
│   ├── models/
│   │   └── license_model.py
│   ├── services/
│   │   └── license_service.py
│   ├── utils/
│   │   └── crypto_utils.py
│   ├── keys/                    # Generated RSA keys (gitignore in production)
│   ├── licenses/                # Generated license files
│   ├── main.py
│   └── requirements.txt
│
├── client-application/          # Licensed application (Docker)
│   ├── controllers/
│   │   └── app_controller.py
│   ├── models/
│   │   └── license_model.py
│   ├── services/
│   │   ├── license_service.py
│   │   └── business_service.py
│   ├── core/
│   │   └── protected_module.pyx  # Cython module
│   ├── utils/
│   │   └── machine_utils.py
│   ├── main.py
│   ├── setup.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── README.md
```

## Quick Start

### 1. Server Setup (License Generation)

```bash
cd server-application
pip install -r requirements.txt

# Generate RSA key pair
python main.py genkeys

# Create a license
python main.py create --customer "Acme Ltd" --expiry 2026-12-31 --out ../client-application/license.lic
```

### 2. Client Setup (Build & Run)

```bash
cd client-application
pip install -r requirements.txt

# Build Cython extension
python setup.py build_ext --inplace

# Copy public key from server
copy ..\server-application\keys\pub.pem .

# Run application
python main.py
```

### 3. Docker Deployment

```bash
cd client-application

# Build Docker image
docker build -t licensed-app:1.0 .

# Run with mounted license (for easy renewal)
docker run -v /path/to/license.lic:/app/license.lic licensed-app:1.0
```

## License Renewal

1. Generate new license on server:
   ```bash
   python main.py create --customer "Acme Ltd" --expiry 2027-12-31 --out new_license.lic
   ```

2. Send `new_license.lic` to customer

3. Customer replaces their mounted license file - no container rebuild needed!

## Security Features

- RSA 4096-bit signatures
- Cython-compiled core modules
- Optional MAC/hostname binding
- Expiry date enforcement
- Public key embedded in compiled module (optional)

## License Binding Options

```bash
# Bind to MAC address
python main.py create --customer "Acme Ltd" --expiry 2026-12-31 --bind-mac AA:BB:CC:DD:EE:FF

# Bind to hostname
python main.py create --customer "Acme Ltd" --expiry 2026-12-31 --bind-hostname server1

# Multiple bindings
python main.py create --customer "Acme Ltd" --expiry 2026-12-31 --bind-mac AA:BB:CC:DD:EE:FF --bind-hostname server1 server2
```
