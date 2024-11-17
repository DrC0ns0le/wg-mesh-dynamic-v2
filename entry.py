import shutil
import json
import os
import modules.keygen as keygen
from jinja2 import Environment, FileSystemLoader

folder_path = 'output'  # Replace with the path to your folder

try:
    shutil.rmtree(folder_path)
except Exception as e:
    pass

# opening config.json config
with open('config.json', 'r') as file:
    # load JSON data from file
    try:
        config = json.load(file)
    except Exception as e:
        print(f"config.json: {e}\nExiting...")
        exit()

# opening data.json working file
try:
    with open('data.json', 'r') as file:
    # load JSON data from file
        try:
            data = json.load(file)
        except Exception as e:
            raise Exception
except Exception as e:
    print(f"data.json: {e}\nCreating new data.json...")
    data = {}


# check for changes in site ids
config_ids = set(site["id"] for site in config["sites"])
data_ids = set(int(key) for key in data.keys())

if config_ids != data_ids:
    new_ids = config_ids - data_ids
    for i in new_ids:
        data[i] = {
            "v4": keygen.generate(),
            "v6": keygen.generate()
        }

    deleted_ids = data_ids - config_ids

    for i in deleted_ids:
        del data[str(i)]

for i, (I, value) in enumerate(data.items()):
    target_length = (len(config_ids) *2 - i - 1)  # Double the target length
    
    if not value.get("preshared_key"):
        psk_list = []
        for j in range(target_length):
            psk_list.append(keygen.preshared())
        value["preshared_key"] = psk_list
    elif len(value.get("preshared_key")) < target_length:
        for j in range(target_length - len(value.get("preshared_key"))):
            value["preshared_key"].append(keygen.preshared())
    elif len(value.get("preshared_key")) > target_length:
        value["preshared_key"] = value["preshared_key"][:target_length]

# save keys to data.json
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2)

# generate the wg.conf files
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("wireguard.tmpl")

for site in config["sites"]:
    
    print(f"Generating configuration files for {site['name']}")
    count = 0
    
    ip_versions = []
    
    match site.get("ip_version", "ds"):
        case "v4":
            ip_versions = ["v4"]
        case "v6":
            ip_versions = ["v6"]
        case "ds":
            ip_versions = ["v4", "v6"]
        
    for ip_version in ip_versions:
        for peer in config["sites"]:
            if site is not peer:   
                
                # generate matching pair of preshared-keys and ports
                if site['id'] < peer['id']:
                    peer_port = site.get("port", config["port"]) + site['id'] + (len(config["sites"])-1 if ip_version == "v6" else 0)
                    preshared_key = data[str(site["id"])]["preshared_key"][peer['id']-site['id']-1 + (len(config["sites"]) if ip_version == "v6" else 0)]
                else:
                    peer_port = site.get("port", config["port"]) + site['id'] - 1 + (len(config["sites"])-1 if ip_version == "v6" else 0)
                    preshared_key = data[str(peer["id"])]["preshared_key"][site['id']-peer['id']-1 + (len(config["sites"]) if ip_version == "v6" else 0)]
                
                listen_port = site.get("port", config["port"]) + count
                count += 1
                
                #first render
                content = template.render(
                    interface_name=f"wg{site['id']}.{peer['id']}_{ip_version}",
                    private_key=data[str(site["id"])][ip_version]["private_key"],
                    peer_ip=peer.get("local", f"10.201.{peer['id']}.0"),
                    peer_ip_v6=peer.get("local_v6", f"fdac:c9:{peer['id']:x}::"),
                    site_subnet=f"10.201.{site['id']}.",
                    preup=site.get("preup", None),
                    postup=site.get("postup", None),
                    predown=site.get("predown", None),
                    postdown=site.get("postdown", None),
                    listen_port=listen_port,
                    mtu=min(peer.get("mtu", float('inf')), site.get("mtu", float('inf')), config["mtu"]) - (20 if ip_version == "v6" else 0),
                    peer_name=peer["name"],
                    peer_public=data[str(peer["id"])][ip_version]["public_key"],
                    preshared_key=preshared_key,
                    site_endpoint= site.get("endpoint", None) and ip_version + "." + site.get("endpoint", None),
                    peer_endpoint= peer.get("endpoint", None) and ip_version + "." + peer.get("endpoint", None),
                    peer_port=peer_port,
                    keep_alive=min(peer.get("keepalive", float('inf')), site.get("keepalive", float('inf')), config["keepalive"]),
                    interface_custom=site.get("interface_custom", None),
                    peer_custom=site.get("peer_custom", None),
                    ip_version=ip_version
                )
                
                intermediate = environment.from_string(content)
                
                #second render for post rules
                content = intermediate.render(
                    listen_port=listen_port,
                    interface_name=f"wg{site['id']}.{peer['id']}_{ip_version}",
                    interface_mss=min(peer.get("mtu", float('inf')), site.get("mtu", float('inf')), config["mtu"]) - 60 # ipv6 header size
                ).strip()
                
                #output configs
                output_directory = f"output/{site['name']}"
                output_file = f"{output_directory}/wg{site['id']}.{peer['id']}_{ip_version}.conf"
                os.makedirs(output_directory, exist_ok=True)
                
                if peer.get("ip_version", "ds") != "ds" and peer.get("ip_version", "ds") != ip_version:
                    continue

                with open(output_file, mode="w", encoding="utf-8") as message:
                    message.write(content)
                    print(f"... wrote {output_file}")