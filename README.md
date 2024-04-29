This repo contains code for a lightweight client to interact with GLPI

# Preparation

# Requirements

- Available glpi instance
- valid user and API token
- prettytable python library

## env variables

store your creds in any env file such as [glpic.env.sample](glpic.env.sample) and set data accordingly

# Installation

```
pip3 install glpic
```

# How to use

```
glpic list computers
```

```
glpic info computer $computer
```

```
glpic list reservations
```

```
glpic info reservation $reservation
```

```
glpic update reservation $reservation -P end=20240601
```
