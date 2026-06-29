from app.tools import registry
from app.tools.dnsx.adapter import DnsxAdapter
from app.tools.ffuf.adapter import FfufAdapter
from app.tools.gobuster.adapter import GobusterAdapter
from app.tools.httpx_probe.adapter import HttpxProbeAdapter
from app.tools.nmap.adapter import NmapAdapter
from app.tools.nuclei.adapter import NucleiAdapter
from app.tools.subfinder.adapter import SubfinderAdapter
from app.tools.whatweb.adapter import WhatWebAdapter

registry.register(SubfinderAdapter())
registry.register(DnsxAdapter())
registry.register(HttpxProbeAdapter())
registry.register(NucleiAdapter())
registry.register(NmapAdapter())
registry.register(GobusterAdapter())
registry.register(WhatWebAdapter())
registry.register(FfufAdapter())
