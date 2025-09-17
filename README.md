This repo contains code for a lightweight client to interact with GLPI and a MCP to consume it from any LLM

# Requirements

- Available glpi instance
- valid user and API token
- prettytable python library

# Installation

```
pip3 install glpic
```

# Using client

Store your creds in any env file such as [glpic.env.sample](glpic.env.sample) and set data accordingly
You can then use the following commands

- List computers

```
glpic list computers
```

- Get information on a specific computer

```
glpic info computer $computer
```

- List reservations

```
glpic list reservations
```

- Get information on a specific reservation


```
glpic info reservation $reservation
```

- Update a given reservations

```
glpic update reservation $reservation -P end=20240601
```

- Update all reservations

```
glpic update reservations
```

# Using MCP

The server is started and configured differently depending on what transport you want to use

For STDIO:

In VSCode for example:
```json
   "mcp": {
        "servers": {
            "glpi": {
                "command": "python3",
                "args": ["/path/to/glpic/src/glpic/mcp_server.py", "--stdio"],
                "env": {
                    "GLPI_URL": "https://server/apirest.php",
                    "GLPI_USER": "myuser",
                    "GLPI_TOKEN": "mytoken"
                }
            }
        }
    }
```

For Streamable HTTP:

Start the server in a terminal:

```
glpimcp
```

Configure the server in your client:

```json
    "rhsupportcli": {
      "transport": "streamable-http",
      "url": "http://your_server:8000"
      "headers": {
        "GLPI_URL": "https://server/apirest.php",
        "GLPI_USER": "myuser",
        "GLPI_TOKEN": "mytoken"
      }
    }
```
