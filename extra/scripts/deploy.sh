#/bin/bash

wall "Deploying new wg.conf"

# Clear old interfaces

cd /etc/wireguard

oldnames=()

for file in *.conf; do
    name=$(basename "$file" .conf)
    oldnames+=("$name")
done

wall "Disabling ${#oldnames[@]} previous wireguard interfaces"

for name in "${oldnames[@]}"; do
    echo "Processing $name..."
    sudo wg-quick down ${name}
    rm ${name}.conf
done

cd /etc/wireguard/staging

names=()

for file in *.conf; do
    name=$(basename "$file" .conf)
    names+=("$name")
done

sleep 2

wall "Deploying ${#names[@]} new wireguard interfaces"

for name in "${names[@]}"; do
    echo "Processing $name..."
    cp ${name}.conf /etc/wireguard/${name}.conf
    sudo wg-quick up ${name}
done

cd ..
rm -rf staging
rm -- "$0"

wall "Deployment completed!"