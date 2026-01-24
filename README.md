# NetBox API Scripts

Python-based automation utilities for **site management** in NetBox (DCIM / IPAM) via its REST API. This repository focuses on **safe, repeatable operations for listing, creating, and deleting sites**.

The scripts are designed to be readable, idempotent where possible, and suitable for demonstrating operational automation patterns.

---

## Purpose

Manually managing sites in NetBox can be error-prone and time-consuming. This project demonstrates:

- Listing existing sites
- Creating new sites safely
- Deleting sites safely
- Handling API errors
- Writing scripts that can be re-run without unintended side effects

All operations currently cover **sites only**.

---

## Real-World Use Case

This repository is intended to:

- Demonstrate safe automation patterns in infrastructure management
- Show how to interact with NetBox programmatically
- Serve as a foundation for integrating site management into broader automation workflows

Operations are limited to site-level management; other NetBox objects (devices, prefixes, IPs) are not yet included.

---

## Architecture & Design

```text
┌──────────────┐      HTTPS       ┌──────────────┐
│ Python CLI   │ ───────────────▶ │ NetBox API   │
│ Scripts      │                  │ (sites only) │
└──────────────┘                  └──────────────┘
```

### Design principles

- **Explicit over implicit**: all behavior is clearly defined
- **Fail fast** on unexpected API responses
- **Idempotent operations** for create/delete
- **Separation of concerns** between API client and script logic

---

## Repository Structure

```text
netbox-api-scripts/
├── scripts/
│   ├── manage_sites.py      # CLI entry point
│   └── netbox_client.py     # NetBox API wrapper
├── requirements.txt
└── README.md
```

- `netbox_client.py` handles API communication
- `manage_sites.py` contains CLI logic and task-specific code

---

## Authentication & Security

Authentication uses a **NetBox API token** and the **NetBox URL** provided via environment variables:

```bash
export NETBOX_API_TOKEN="<your-token>"
export NETBOX_URL="https://netbox.example.com"
```

Best practices:

- Tokens are never hard-coded
- Sensitive values are excluded from version control
- HTTPS is required for all API communication

---

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Supported Python version:

- Python 3.9+

---

## Usage Example

```bash
python scripts/manage_sites.py --list
python scripts/manage_sites.py --create <site-name>
python scripts/manage_sites.py --delete <site-name>
```

Operations are idempotent where possible, and scripts are safe to re-run for demonstration and testing purposes.

---

## Error Handling & Reliability

Includes safeguards for:

- HTTP status code validation
- Clear error messages on API failures
- Defensive handling of empty or unexpected responses

Failure scenarios considered:

- Invalid or expired API tokens
- Network timeouts
- Partial API responses

---

## Limitations

- Supports only **site objects** in NetBox
- Does not include devices, prefixes, or IPs
- Error handling is explicit but minimal
- No persistent state outside NetBox

These limitations are intentional to keep scripts understandable and safe.

---

## Future Improvements

- Add structured logging
- Retry logic with exponential backoff
- Support for additional NetBox objects
- Unit tests with mocked API responses
