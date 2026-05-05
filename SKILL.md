---
name: glpi
description: Use this skill to manage GLPI resources — reservations, computers, and users
---

# GLPI skill

Use this skill to manage GLPI resources: reservations, computers, and users.

## Usage

Run glpic from regular PATH. Always source credentials first.

## Available Commands

### Reservations

```bash
# List current user's reservations
glpic list reservations

# List another user's reservations
glpic list reservations -P user=someuser

# Create a reservation for a computer (defaults to current user, 30-day end date)
glpic create reservation COMPUTER_NAME

# Create with force (deletes existing reservation if needed)
glpic create reservation COMPUTER_NAME -f

# Create a reservation with specific parameters
glpic create reservation COMPUTER_NAME -P user=someuser -P end=2026-06-01 -P comment="testing"

# Update all current user's reservations (extends end date by 30 days if no params given)
glpic update reservations

# Update specific reservations by ID
glpic update reservations 123 456

# Update reservation with specific parameters
glpic update reservations 123 -P end=2026-07-01 -P user=someuser

# Delete reservations (asks for confirmation)
glpic delete reservation 123 456

# Delete without confirmation
glpic delete -y reservation 123
```

### Computers

```bash
# List all computers
glpic list computers

# List computers filtered by CPU model or minimum memory
glpic list computers -P cpumodel=xeon -P memory=64000

# Limit number of results
glpic list computers -P number=10

# Get detailed info about a specific computer (by name or ID)
glpic info computer COMPUTER_NAME

# Update a computer's fields
glpic update computer COMPUTER_NAME -P comment="new comment"
```

### Users

```bash
# List all users
glpic list users

# List users with filter
glpic list users -P is_active=1
```

## Parameters

The `-P` flag accepts key=value pairs and can be specified multiple times.

| Context | Parameter | Description |
|---------|-----------|-------------|
| Reservations | user | Target user (defaults to authenticated user) |
| Reservations | end | End date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) |
| Reservations | comment | Reservation comment |
| Computers | cpumodel | Filter by CPU model substring |
| Computers | memory | Filter by minimum memory (in MB) |
| Computers | number | Limit number of results |

## Command Aliases

Commands accept aliases: `add`=`create`, `remove`=`delete`, `get`=`list`. Singular and plural forms are interchangeable (`reservation`/`reservations`, `computer`/`computers`, `user`/`users`).

## Behavior

1. Source the file ~/glpic.env for credentials before running any command.
2. Report the script's text output as-is to the user.
