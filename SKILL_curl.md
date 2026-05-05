---
name: glpi-api
description: Use this skill to manage GLPI resources (reservations, computers, users) via direct curl calls to the GLPI REST API — no Python dependency needed
---

# GLPI API skill

Manage GLPI resources directly via curl against the GLPI REST API. Claude parses the JSON responses directly — no jq needed.

## Credentials

Source `~/glpic.env` before any call. It exports:
- `GLPI_URL` — base API URL (e.g. `https://glpi.example.com/apirest.php`)
- `GLPI_TOKEN` — user API token
- `GLPI_USER` — username

## Authentication

Every session starts by obtaining a session token. All subsequent calls use that token.

```bash
source ~/glpic.env

# Init session — returns JSON with session_token field
curl -sk "$GLPI_URL/initSession" \
  -H "Content-Type: application/json" \
  -H "Authorization: user_token $GLPI_TOKEN"
```

Extract the `session_token` value from the response and use it in all subsequent requests:

```bash
-H "Session-Token: SESSION_TOKEN_VALUE"
```

## Listing resources

The API returns paginated results. Use `range=0-99999` to get all items.

```bash
# List all users
curl -sk "$GLPI_URL/User?range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# List all reservations
curl -sk "$GLPI_URL/Reservation?range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# List all computers (search endpoint with uid_cols for full details)
curl -sk "$GLPI_URL/search/Computer?uid_cols&range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# List reservation items (maps computers to reservable items)
curl -sk "$GLPI_URL/ReservationItem?uid_cols&range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"
```

## Getting info on a single resource

When fetching a single item by ID, do NOT append the range parameter.

```bash
# Get a specific user by ID
curl -sk "$GLPI_URL/User/42" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# Get a specific computer by ID
curl -sk "$GLPI_URL/Computer/123" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# Get a specific reservation by ID
curl -sk "$GLPI_URL/Reservation/456" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# Get a reservation item by ID (links reservable items to computers)
curl -sk "$GLPI_URL/ReservationItem/789" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"
```

## Searching computers

Use the search endpoint with criteria to find computers by name or ID.

```bash
# Search computer by name (field 1 = name)
curl -sk "$GLPI_URL/search/Computer?criteria[0][link]=AND&criteria[0][field]=1&criteria[0][searchtype]=contains&criteria[0][value]=HOSTNAME&uid_cols&range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# Search computer by ID (field 2 = id)
curl -sk "$GLPI_URL/search/Computer?criteria[0][link]=AND&criteria[0][field]=2&criteria[0][searchtype]=contains&criteria[0][value]=123&uid_cols&range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"
```

Results are in the `data` array of the JSON response.

## Finding a user by name

Fetch all users and parse the JSON response to find the matching user by `name` field.

```bash
curl -sk "$GLPI_URL/User?range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"
```

## Creating a reservation

Requires a `reservationitems_id` (not the computer ID directly). To find it:

1. Search the computer to get its ID from the response
2. Fetch ReservationItems and find the entry with `itemtype=Computer` and `items_id` matching the computer ID
3. Use that entry's `id` as `reservationitems_id`

```bash
# Step 1: Search computer to get its ID
curl -sk "$GLPI_URL/search/Computer?criteria[0][link]=AND&criteria[0][field]=1&criteria[0][searchtype]=contains&criteria[0][value]=HOSTNAME&uid_cols&forcedisplay[0]=2&range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# Step 2: Get reservation items and find the one matching the computer ID
curl -sk "$GLPI_URL/ReservationItem?uid_cols&range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# Step 3: Get user ID by listing users
curl -sk "$GLPI_URL/User?range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"

# Step 4: Create the reservation using IDs extracted from previous responses
curl -sk "$GLPI_URL/Reservation" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE" \
  -X POST \
  -d '{"input": {"reservationitems_id": RESERVATION_ITEM_ID, "users_id": USER_ID, "begin": "YYYY-MM-DD HH:MM:SS", "end": "YYYY-MM-DD HH:MM:SS", "comment": "reservation for USERNAME"}}'
```

Default behavior: `begin` = now, `end` = 30 days from now.

## Updating a reservation

```bash
curl -sk "$GLPI_URL/Reservation/RESERVATION_ID" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE" \
  -X PUT \
  -d '{"input": {"end": "2026-07-01 00:00:00"}}'
```

## Deleting a reservation

```bash
curl -sk "$GLPI_URL/Reservation/RESERVATION_ID" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE" \
  -X DELETE
```

## Updating a computer

```bash
curl -sk "$GLPI_URL/Computer/COMPUTER_ID" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE" \
  -X PUT \
  -d '{"input": {"comment": "new comment"}}'
```

## Filtering current reservations for a user

To list active reservations: fetch all reservations and filter by `users_id` matching the user and `end` date in the future.

```bash
curl -sk "$GLPI_URL/Reservation?range=0-99999" \
  -H "Content-Type: application/json" \
  -H "Session-Token: SESSION_TOKEN_VALUE"
```

Parse the JSON response to keep only entries where `users_id` matches and `end` is after the current date.

## Behavior

1. Source `~/glpic.env` for credentials before any call.
2. Always init a session first to get the session token.
3. Parse JSON responses directly — do not use jq or other external tools.
4. Report results as-is to the user.
5. Use `-sk` flags on curl (silent + skip TLS verification, matching the CLI behavior).
