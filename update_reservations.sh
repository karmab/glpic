#!/usr/bin/env bash

reservations="9833 9836 9837 9838 9839"

now=$(date +%Y-%m-%d)
one_month=$(date -d "$current_date + 1 month" +%Y-%m-%d)

for reservation in $reservations ; do
  glpi update reservation $reservation -P end="$one_month 00:00:00"
done
