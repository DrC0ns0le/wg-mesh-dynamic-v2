#!/bin/bash

# Find all WireGuard configuration files
config_files=$(find /etc/wireguard -name "wg[0-9].[0-9]_v[0-9].conf")

for config_file in $config_files; do
    # Extract interface name by removing .conf extension
    interface=$(basename "$config_file" .conf)
    
    # Extract site_id value from the interface name
    site_id=$(echo "$interface" | cut -d'.' -f2 | cut -d'_' -f1)
    
    # Ping target IP
    target_ip="10.201.${site_id}.1"
    
    tries=0
    while [ $tries -lt 3 ]; do
        if /bin/ping -c 1 -W 2 "$target_ip"; then
            logger -t "wg-watchdog" "WireGuard interface $interface to site $site_id is working"
            break
        else
            logger -t "wg-watchdog" "WireGuard interface $interface to site $site_id is down, restarting..."
            sudo wg-quick down "$interface"
            sleep 3
            sudo wg-quick up "$interface"
            logger -t "wg-watchdog" "WireGuard interface $interface to site $site_id restarted"
            break
        fi
        tries=$((tries+1))
    done
done