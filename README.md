# About

Lightweight GLPI client


# Requirements

- Available glpi instance
- Valid user and API token

# Installation

You can either run as a container or install dependencies locally

```
pip3 install glpic
```

# Using client

Store your creds in any env file such as [glpic.env.sample](glpic.env.sample) and set data accordingly. You can then use `glpic` and access similar functions

# Skill

Just use the skill


# MCP


First start the server in a terminal:

```
glpimcp
```

or via a container (with additional env variables to avoid defining headers on client side)

```
podman run -p 8000:8000 -d --name glpi --entrypoint=/usr/local/bin/glpimcp quay.io/karmab/glpic
```

You can also set env variables prior to launching or in the container to avoid defining headers on client side). For instance

```
podman run -p 8000:8000 -d --name glpi -e GLPI_URL=https://glpiserver/apirest.php -e GLPI_USER=myser -e GLPI_TOKEN=mytoken --entrypoint=/usr/local/bin/glpimcp quay.io/karmab/glpic
```


You can then point to the server from your client with a modified snippet and specifying credentials via headers if needed

```
claude mcp add --transport http glpi http://your_server:8000/mcp -H "GLPI_URL: https://myserver/apirest.php" -H "GLPI_USER: myuser" -H "GLPI_TOKEN: mytoken"
```

| Available tools   |
|-------------------|
|create_reservation |
|delete_reservation |
|info_computer      |
|info_reservation   |
|get_user           |
|list_computers     |
|list_reservations  |
|list_users         |
|update_computer    |
|update_reservation |
