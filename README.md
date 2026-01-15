# NetBox API Scripts

Python scripts demonstrating NetBox API interactions: listing sites, creating sites with metadata, and handling idempotent operations.

## Features

The scripts performs the following actions:

* ✅ List all existing NetBox sites
* ✅ Create a new site named **`demo-site-1`**
  * Status: `Planned`
  * Tag: `new_dc_buildout`
* ✅ Safely handle errors if the site already exists (idempotent behavior)

The script can be re-run multiple times without causing duplicate objects.

---

## Requirements

* Python **3.8+**
* NetBox **API Token**
* NetBox reachable via HTTP/HTTPS

Python dependencies:

* `requests`

---
