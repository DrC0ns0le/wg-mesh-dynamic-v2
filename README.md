# WireGuard Mesh Configuration Generator

A Python-based tool for generating WireGuard mesh network configurations with support for dynamic routing. Unlike traditional WireGuard mesh setups, this tool creates separate interfaces for each peer, enabling advanced routing capabilities and enhanced network resilience.

## Key Differentiators

- **Separate Interfaces**: Creates individual WireGuard interfaces for each peer instead of combining them into a single interface
- **Dynamic Routing Support**: Designed to work with protocols like BGP, OSPF, or RIP for redundant routes
- **Route Flexibility**: Overcomes WireGuard's AllowedIPs routing limitations by allowing overlapping network routes
- **High Availability**: Interface isolation ensures that issues with one connection don't affect others

## Dynamic Routing Integration

This tool is designed to work with dynamic routing protocols:

- BGP
- OSPF
- RIP

The separate interface approach allows:

- Multiple routes to the same subnet
- OS-level routing decisions
- Independent interface management
- Route redundancy

## Features

- 🔀 Individual WireGuard interface per peer connection
- 🌐 Full IPv4 & IPv6 dual-stack support
- 🔑 Automatic key management and generation
- 📝 Template-based configuration using Jinja2
- 🎯 Site-specific customization options
- 🔄 Persistent key storage
- 🚦 Dynamic port allocation
- 🛠️ Customizable up/down scripts
- 📁 Organized output structure for automation tools
- 🔍 Automatic peer discovery and configuration

## Network Architecture

### Default Network Scheme

- Overlay Network: `10.201.0.0/16` (IPv4) and `fdac:c9::/56` (IPv6)
- Site Networks: `10.X.0.0/16` where X is the site ID
- Site IPs:
  - IPv4: `10.201.X.1/24` (X = site ID)
  - IPv6: `fdac:c9:X::/64` (X = site ID in hex)

### Interface Naming Convention

Format: `wgS.P_vI` where:

- S: Source site ID
- P: Peer site ID
- I: IP version (v4/v6)

Example: `wg1.2_v4` = Site 1 to Peer 2 IPv4 interface

## Prerequisites

- Python 3.x
- Jinja2 templating engine
- WireGuard installed on target systems

## Installation

1. Clone this repository:

```bash
git clone https://github.com/DrC0ns0le/wg-mesh-dynamic-v2.git
cd wg-mesh-dynamic-v2
```

2. Install required dependencies:

```bash
pip install jinja2
```

## Configuration

### config.json Structure

```json
{
  "port": 51820,
  "mtu": 1420,
  "keepalive": 25,
  "sites": [
    {
      "id": 1,
      "name": "site1",
      "endpoint": "site1.example.com",
      "ip_version": "ds",
      "local": "10.1.0.0",
      "local_v6": "fdac:c9:1::",
      "mtu": 1420,
      "keepalive": 25,
      "preup": ["custom-preup-command"],
      "postup": ["custom-postup-command"],
      "predown": ["custom-predown-command"],
      "postdown": ["custom-postdown-command"],
      "interface_custom": ["custom-interface-setting"],
      "peer_custom": ["custom-peer-setting"]
    }
  ]
}
```

### Configuration Files

1. **config.json**: Main configuration file (required)
   - Global settings (port, MTU, keepalive)
   - Site-specific configurations
   - Network preferences
2. **data.json**: Key storage file (auto-generated)

   - Stores WireGuard keys between runs
   - Contains public/private keypairs
   - Manages pre-shared keys
   - Should be secured or deleted after deployment

3. **templates/wireguard.tmpl**: Configuration template
   - Jinja2 template for WireGuard configs
   - Defines interface structure
   - Contains routing rules
   - Customizable for specific needs

## Usage

1. Create your configuration:

```bash
cp config.json.example config.json
# Edit config.json with your site details
```

2. Generate configurations:

```bash
python entry.py
```

3. Find your configuration files in the `output` directory:

```
output/
├── site1/
│   ├── wg1.2_v4.conf
│   ├── wg1.2_v6.conf
│   ├── wg1.3_v4.conf
│   └── wg1.3_v6.conf
...
```

## Security Considerations

- Pre-shared keys are automatically generated for all peer connections
- Private keys are stored in `data.json` - secure appropriately
- Consider using environment variables for sensitive data
- Delete `data.json` after deployment if desired

## Troubleshooting

### Common Issues

1. **Port Conflicts**

   - Check base port availability
   - Verify port range doesn't overlap
   - Ensure unique ports per interface

2. **Routing Issues**

   - Verify routing protocol configuration
   - Check interface UP/DOWN states
   - Confirm IP forwarding is enabled
   - Validate firewall rules

3. **Key Management**
   - Backup `data.json` before modifications
   - Verify key permissions
   - Check for key rotation needs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas of interest:

- Additional routing protocol integration
- Enhanced templating options
- Security improvements
- Documentation updates

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- WireGuard® is a registered trademark of Jason A. Donenfeld
- Thanks to the WireGuard and Python communities
- Part of my University Final Year Project
