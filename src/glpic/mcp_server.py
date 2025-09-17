import argparse
# import os
from glpic import Glpic
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_http_headers

mcp = FastMCP("glpimcp")


@mcp.tool()
def list_reservations(context: Context,
                      parameters: dict) -> dict:
    """List glpi reservations"""
    url = get_http_headers().get('glpi_url')
    user = get_http_headers().get('glpi_user')
    api_token = get_http_headers().get('glpi_token')
    glpic = Glpic(url, user, api_token)
    return glpic.list_reservations(overrides=parameters)


def main():
    parser = argparse.ArgumentParser(description="glpimcp")
    parser.add_argument("--port", type=int, default=8000, help="Localhost port to listen on")
    parser.add_argument("-s", "--stdio", action='store_true')
    args = parser.parse_args()
    parameters = {'transport': 'stdio'} if args.stdio else {'transport': 'http', 'host': '0.0.0.0', 'port': args.port}
    mcp.run(**parameters)


if __name__ == "__main__":
    main()
