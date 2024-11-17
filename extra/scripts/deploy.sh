#/bin/bash

sleep 10

cd ./staging

names=()

for file in *.conf; do
    name=$(basename "$file" .conf)
    names+=("$name")
done

for name in "${names[@]}"; do
    echo "Processing $name..."
    sudo wg-quick down ${name}
    sleep 0.5
    cp ${name}.conf /etc/wireguard/${name}.conf
    sudo wg-quick up ${name}
done

cd ..
rm -rf staging
rm -- "$0"