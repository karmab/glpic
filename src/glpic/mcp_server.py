import argparse
# import os
from glpic import Glpi
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_http_headers as h

mcp = FastMCP("glpimcp")


@mcp.tool()
def create_reservation(context: Context,
                       user: str, computer: str, overrides: dict = {}) -> dict:
    """Create glpi reservation"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.create_reservation(user, computer, overrides)


@mcp.tool()
def delete_reservation(context: Context,
                       reservation: str) -> dict:
    """Delete glpi reservation"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.delete_reservation(reservation)


@mcp.tool()
def info_computer(context: Context,
                  computer: str, overrides: dict = {}) -> dict:
    """Get info on glpi computer"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.info_computer(computer)


@mcp.tool()
def info_reservation(context: Context,
                     reservation: str) -> dict:
    """Get info on glpi reservation"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.info_reservation(reservation)


@mcp.tool()
def get_user(context: Context,
             user: str) -> dict:
    """Get info on glpi user"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.get_user(user)


@mcp.tool()
def list_computers(context: Context,
                   overrides: dict) -> list:
    """List glpi computers"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.list_computers(overrides)


@mcp.tool()
def list_reservations(context: Context,
                      user: str) -> list:
    """List glpi reservations"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.list_reservations(user)


@mcp.tool()
def list_users(context: Context,
               overrides: dict = {}) -> list:
    """List glpi users"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.list_users(overrides)


@mcp.tool()
def update_computer(context: Context,
                    computer: str, overrides: dict) -> dict:
    """Update glpi computer"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.update_computer(computer, overrides)


@mcp.tool()
def update_reservation(context: Context,
                       user: str, reservation: str, overrides: dict = {}) -> dict:
    """Create glpi reservation"""
    glpic = Glpi(h().get('glpi_url'), h().get('glpi_user'), h().get('glpi_token'))
    return glpic.update_reservation(user, reservation, overrides)


def main():
    parser = argparse.ArgumentParser(description="glpimcp")
    parser.add_argument("--port", type=int, default=8000, help="Localhost port to listen on")
    parser.add_argument("-s", "--stdio", action='store_true')
    args = parser.parse_args()
    parameters = {'transport': 'stdio'} if args.stdio else {'transport': 'http', 'host': '0.0.0.0', 'port': args.port}
    mcp.run(**parameters)


if __name__ == "__main__":
    main()
