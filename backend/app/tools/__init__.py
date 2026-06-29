from app.tools import registry
from app.tools.gobuster.adapter import GobusterAdapter
from app.tools.httpx_probe.adapter import HttpxProbeAdapter
from app.tools.nmap.adapter import NmapAdapter
from app.tools.nuclei.adapter import NucleiAdapter
from app.tools.subfinder.adapter import SubfinderAdapter
from app.tools.whatweb.adapter import WhatWebAdapter

registry.register(SubfinderAdapter())
registry.register(HttpxProbeAdapter())
registry.register(NucleiAdapter())
registry.register(NmapAdapter())
registry.register(GobusterAdapter())
registry.register(WhatWebAdapter())
