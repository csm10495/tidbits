#!/usr/bin/env bash

# Explanation:
# Send a UDP packet requesting a NTP timestamp back
# Then cheaply parse (and ignore errors!)
# https://datatracker.ietf.org/doc/html/rfc958
# We get the receive timestamp's integer part (ignoring fractionals) .. starts at byte 32 and goes for 4 bytes and is big endian
# ntp gives the time back since the start of the year 1900. Unix timestamps start at 1970. Subtract 70 years (2208988800) to get a unix timestamp

date --date @$(( $(printf '\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' | \
nc -u time.google.com 123 | \
od -An -j 32 -N 4 -t u4 --endian=big | xargs) - 2208988800 ))


# Example:
# ./get_time.sh
#Sat 24 Aug 2024 04:24:50 PM PDT