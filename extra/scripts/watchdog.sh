#!/bin/bash

cd /etc/wireguard || exit 1

# Initialize an array to store the Y values
wg_interfaces=()

# Loop through all .conf files
for file in wg*.conf; do
    [[ -f "$file" ]] || continue
    name=$(basename "$file" .conf)
    wg_interfaces+=("$name")
done

for wg_interface in "${wg_interfaces[@]}"; do
    # Extract the site id using regex
    if [[ $wg_interface =~ wg([0-9]+)\.([0-9]+)_v([0-9]+) ]]; then
        local="${BASH_REMATCH[1]}"
        site="${BASH_REMATCH[2]}"
        ip_version="${BASH_REMATCH[3]}"
    else
        logger -t "wg-watchdog" "Unsupported interface name format: $wg_interface"
        continue
    fi
    tries=0
    while [ $tries -lt 3 ]; do
        if /bin/ping -c 1 -W 2 -I "10.201.${local}.${ip_version}" "10.201.${site}.${ip_version}"; then
            logger -t "wg-watchdog" "wireguard to site ${site} via IPv${ip_version} working"
            break
        else
            sudo wg-quick down "${wg_interface}"
            sleep 3
            sudo wg-quick up "${wg_interface}"

            logger -t "wg-watchdog" "wireguard to site ${site} restarted"
            break
        fi
        tries=$((tries+1))
    done
done