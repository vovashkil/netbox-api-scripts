"""
manage_sites.py

Unified CLI tool for managing NetBox sites.

Subcommands:
    list    - List all sites
    create  - Create a new site
    delete  - Delete a site

Usage:
    python manage_sites.py list [-v]
    python manage_sites.py create --name demo-site-1 [--status planned] [--tag tag1,tag2]
    python manage_sites.py delete --name demo-site-1
"""

import argparse
from netbox_client import NetBoxClient


def list_sites(args):
    """
    List all sites in NetBox.

    If verbose is enabled, prints detailed site info.
    """
    client = NetBoxClient()
    response = client.list_sites()

    if not response["results"]:
        print("No sites found.")
        return

    print("Existing sites:")
    for site in response["results"]:
        if args.verbose:
            tags = [tag['name'] for tag in site.get('tags', [])]
            print(f"- Name: {site['name']}, Slug: {site['slug']}, Status: {site['status']['label']}, Tags: {tags}")
        else:
            print(f"- {site['name']}")


def create_site(args):
    """
    Create a site in NetBox, idempotent.

    Does not create the site if it already exists.
    """
    client = NetBoxClient()
    tags = [tag.strip() for tag in args.tag.split(",")]

    existing_site = client.get_site_by_name(args.name)
    if existing_site:
        print(f"Site '{args.name}' already exists. No action taken.")
        return

    print(f"Creating site '{args.name}'...")
    client.create_site(
        name=args.name,
        status=args.status,
        tags=tags,
    )
    print("Site created successfully.")


def delete_site(args):
    """
    Delete a site in NetBox, idempotent.

    Exits gracefully if the site does not exist.
    """
    client = NetBoxClient()
    existing_site = client.get_site_by_name(args.name)
    if not existing_site:
        print(f"Site '{args.name}' does not exist. No action taken.")
        return

    site_id = existing_site["id"]
    print(f"Deleting site '{args.name}' (ID: {site_id})...")

    try:
        client._request("DELETE", f"/api/dcim/sites/{site_id}/")
        print("Site deleted successfully.")
    except RuntimeError as exc:
        print(f"Failed to delete site: {exc}")


def main():
    """Parse CLI arguments and dispatch to subcommands."""
    parser = argparse.ArgumentParser(description="Manage NetBox sites")
    subparsers = parser.add_subparsers(title="subcommands", dest="command", required=True)

    # List subcommand
    parser_list = subparsers.add_parser("list", help="List all NetBox sites")
    parser_list.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed site info (slug, status, tags)"
    )
    parser_list.set_defaults(func=list_sites)

    # Create subcommand
    parser_create = subparsers.add_parser("create", help="Create a NetBox site")
    parser_create.add_argument("--name", required=True, help="Name of the site to create")
    parser_create.add_argument("--status", default="planned", help="Site status (default: planned)")
    parser_create.add_argument("--tag", default="new_dc_buildout", help="Comma-separated tags (default: new_dc_buildout)")
    parser_create.set_defaults(func=create_site)

    # Delete subcommand
    parser_delete = subparsers.add_parser("delete", help="Delete a NetBox site")
    parser_delete.add_argument("--name", required=True, help="Name of the site to delete")
    parser_delete.set_defaults(func=delete_site)

    # Parse args and run
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()