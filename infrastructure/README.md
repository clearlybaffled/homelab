# Infrastructure

## Layout 

### Hardware

- Location: America / North East
- Network:
  - ISP: Verizon FIOS (100MB/100MB)
  - WiFi: Netgear R6700 with DD-WRT
  - Switch: Cisco Catalyst 3750-X 48 port 10/100/1000 PoE
  - Gateway/Firewall: OpnSense 23

#### Systems:

|Hostname|Use(s)|Operating System|Hardware|RAM|Storage|Other|
|:-------|:-----|:---------------|:-------|:---|:-----------|:---------|
|`growler`|Gateway/Firewall| FreeBSD 13.1-RELEASE | ASUS Z170-M Pentium G440 3.3GHz| 8GB| 250GB NVMe ||
|`parche`|Server|Debian 11.7|ASUS Z170-A i7-6700 4.0GHz|32GB|<ul><li>250GB SSD<li>24TB HDDs</ul>| Happauge 1609 WinTV-quadHD tuner|
|`barb`|Desktop|Windows 10 Pro|Gigabyte Z370 AORUS<br/> Intel i5-8600K @ 3.60 GHz| 64GB | <ul><li>500GB NVMe<li>250GB SSD</ul>| Zotac GeForce GTX 1660 Super 6GB GDDR6|
|`tirante`|Workstation|Ubuntu 22.04 LTS| WSL version 2 on `barb`| 32GB | 375MB | |
|`seawolf`|Workstation|Windows 10 Home|Dell XPS 13|16GB|250GB HDD||

  #### Host naming conventions
  
  All of the physical and virtual hosts are named for the [WW2 submarines commanded](ww2-sub-moh-uri) by a [Congressional Medal of Honor](https://mohmuseum.org/the-medal/) recipient. The Kubernetes cluster is named `gato`  for the first major class of submarines built by the U.S. for use in WW2. I wanted to name something `wahoo`, after [one](wahoo-uri) of the most successful and prolific submarines of the pacific theater, but she did not meet the requirement of having been commanded by a MoH recipient. So, anything inside the cluster that gets named will be a Gato-class submarine. Maybe the hajimari homepage, but we're not quite there yet ...


## Usage guide

Prerequisites: 
 - python-3.9+
 - pip
 - virtualenv

Configure cluster using the playbook
```shell
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -U -r requirements.txt
# Don't think this is needed
# $ ansible-galaxy install -r requirements.yaml
$ ansible-playbook playbooks/cluster.yml
```


Main features include:

- Completely sets up a control plane host from nothing to fully running
- Switching to using localhost for tasks execution once direct access to the control plane itself is no longer needed
  
Still needs to:

- Be able to handle setting up additional control plane hosts (it might, but probably doesn't). (It definitely won't join a new control plane, I'm more wondering how much of the setup was tweaked for the first host..)


[wahoo-uri]: https://en.wikipedia.org/wiki/USS_Wahoo_(SS-238)
[ww2-sub-moh-uri]: https://www.navalsubleague.org/links/historymuseums/submarine-force-medal-honor-recipients/
