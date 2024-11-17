# WireGuard Mesh Configuration Generator V2

Wireguard Mesh Configuration Generator for Dynamic Routing

This is a simple project aims to simplify the setup of WireGuard mesh site-to-site connections by generating configuration files. Unlike similar projects, it creates separate interfaces for each peer instead of combining them into a single interface.

This approach is necessary due to WireGuard's limitation of only routing traffic defined within AllowedIPs without allowing overlaps. This meant that multiple routes to the same subnet is not possible. By employing separate interfaces, this allows for overlapping network routes, and lets the routing decision to be made at the OS level. Another advantages is that if the interface needs to be taken down or restarted for whatever reason, the connection to other sites are not affected.

This project is intended to be used inconjunction with dynamic routing protocols such as BGP, OSPF or RIP for creation & advertising of redundant routes. Should you not want that, you would need to configure your own static routes by creating your own routes by specifying custom PostUp in the configuration.

This Python script generates WireGuard configuration files based on a template file located in the "template" folder. The main goal is to create WireGuard interfaces for each peer at each site. Users simply need to customize the `config.json` file to add the necessary information for each site, and the script will handle the rest, generating all the required configuration files.

Disclaimer: This is originally a simple script I developed for my personal use, but thought it could be useful to some. Use at your own risk!

## Features

- For every peer in each site, a unique wireguard interface is created.
- Supports IPv4 & IPv6 dual stack.
- No NAT by default.
- Customisable `[Interface]` and `[Peer]` entries, as well as endpoints, keepalive, mtu and pre/post up/down rules per site.
- Predictable interface naming.
- Automatically generates next available listening port for each interface starting from the port defined in `config.json`
- Automatically generates public/private key pairs for each site and unique preshared keypairs for each site-peer pair.
- Seperate file for private & public key pair for each site, and preshared-key pairs, allowing for key-rotation.
- Table is set to off in template, routes for the interfaces is defined and created through UpDown rules
- Configuration files for each site is stored in seperate folders within the `output` folder. This is to facilitate automation to deploy the configuration files through tools like Ansible.
- Supports up to 200 sites (could be increased)

## Assumptions & Convention

These are the assumptions/conventions that has been made,

- Assumes each site uses a `10.X.0.0/16` network, where X is the site ID.
- Uses a mesh overlay network in the `10.201.0.0/16` and `fdac:c9::/56` subnet.
- Site IP: `10.201.X.1/24` & `fdac:c9::2/64`, where X is the site ID(hex in IPv6).
- By default, the interface allows all traffic(`0.0.0.0/0` & `::/0`), routing is configured seperately.
- Each site is assumed to peer with all other sites.

Each site must have an ID defined in the `config.json` file. The WireGuard interface will take on the following format:

- Interface name: `wgS.P_vI`, where S is the site ID, P is the peer ID, I is the network IP version.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/DrC0ns0le/wg-mesh-dynamic.git
```

## Usage

0. `config.json.example` has been provided as an example. Copy this file to `config.json` and edit it.
1. Customize the `config.json` file to include information about each site.
2. Run the script:

```bash
python entry.py
```

3. The generated configuration files will be stored in the `output` folder. Within the `output` folder, there will be a folder named after each site, containing the configuration files (`wgS.P.conf`) for each peer at that site, where S is the site ID and P is the peer ID.

## Configuration Files

### `config.json`

Users can specify the following information for each site:

- name (required)
- id (required)
- endpoint
- keepalive
- mtu
- post/pre up/down
- interface_custom
- peer_custom
- local
- local_v6

You may refer to config.json.example

### `data.json`

This file stores all generated keys by the script to persist them between runs. You should treat this file like a password file. For security reasons, this file may be deleted after generating the configurations

### `templates/wireguard.tmpl`

This is the template file used for generating the WireGuard configurations. It is rendered using Jinja based on values from `data.json`. UpDown rules for adding routes and creating iptable forwarding rules are included here. Customize this template file according to your requirements.

## Example

Suppose we have three sites:

- Site 1 (Site Name: siteA, Site ID: 0, Dual Stack)
  - Peer 1 (Site ID: 1)
  - Peer 2 (Site ID: 2)
- Site 2 (Site Name: siteB, Site ID: 1, V4 Only)
  - Peer 1 (Site ID: 0)
  - Peer 2 (Site ID: 2)
- Site 3 (Site Name: siteC, Site ID: 2, Dual Stack)
  - Peer 1 (Site ID: 0)
  - Peer 2 (Site ID: 1)

After customizing the `config.json` file and running the script, the generated configuration files will be organized as follows:

```
output/
│
├── siteA/
│   ├── wg0.1_v4.conf
│   ├── wg0.1_v6.conf
│   └── wg0.2_v4.conf
│
├── siteB/
│   ├── wg1.0_v4.conf
│   ├── wg1.0_v6.conf
│   └── wg1.2_v4.conf
│
└── siteC/
    ├── wg2.0_v4.conf
    └── wg2.1_v4.conf

```

## Contributing

Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
