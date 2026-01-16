# NetBox API Scripts

This repository contains a Python CLI tool to manage NetBox sites via the **NetBox REST API**.  

The main script, `manage_sites.py`, supports the following operations:

- **list**: List all sites
- **create**: Create a new site
- **delete**: Delete a site

The scripts are designed to be **idempotent** and safe to re-run.

---

## Repository Structure

```text
netbox-api-scripts/
├── README.md
├── requirements.txt
└── scripts/
    ├── manage_sites.py
    └── netbox_client.py
```

---

## Prerequisites

- Python 3.8+
- NetBox instance accessible via HTTP/HTTPS
- NetBox API Token (set as environment variable)

---

## Step-by-Step Instructions

### 1. Clone the repository

```bash
git clone https://github.com/vovashkil/netbox-api-scripts.git
cd netbox-api-scripts
```

---

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
```

---

### 3. Activate the virtual environment

- On **Linux/macOS**:

```bash
source .venv/bin/activate
```

- On **Windows (PowerShell)**:

```powershell
.\.venv\Scripts\Activate.ps1
```

If you get an execution policy error, run once (as your user):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Then activate again.

---

### 4. Install required dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure environment variables

Set the following environment variables with your NetBox information:

```bash
export NETBOX_URL="http://<your-netbox-url>"
export NETBOX_API_TOKEN="<your-api-token>"
```

On Windows (PowerShell):

```powershell
$env:NETBOX_URL="http://<your-netbox-url>"
$env:NETBOX_API_TOKEN="<your-api-token>"
```

---

### 6. Run scripts

Navigate to the `scripts` folder to run the CLI tool:

```bash
cd scripts
```

#### a) List all sites

```bash
python manage_sites.py list
```

Add `-v` for verbose output:

```bash
python manage_sites.py list -v
```

#### b) Create a new site

```bash
python manage_sites.py create --name demo-site-1
```

Optional arguments:

```bash
python manage_sites.py create --name demo-site-2 --status active --tag "new_dc_buildout,urgent"
```

#### c) Delete a site

```bash
python manage_sites.py delete --name demo-site-1
```

---

## Notes

- The `create` and `delete` commands are **idempotent**: running them multiple times will not cause errors or duplicate sites.
- Tags can be provided as a **comma-separated list**.
- The CLI tool can be extended to manage devices, racks, prefixes, and other NetBox objects.

---

## License

This project is provided for **demonstration purposes**.
