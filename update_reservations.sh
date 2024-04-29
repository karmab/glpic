#!/usr/bin/env bash

reservations="9833 9836 9837 9838 9839 11009 11011 11012 729 730 731 732 733 1363 8317 11010 11018 11019"

now=$(date +%Y-%m-%d)
one_month=$(date -d "$current_date + 1 month" +%Y-%m-%d)

for reservation in $reservations ; do
  glpic update reservation $reservation -P end="$one_month 00:00:00"
done
