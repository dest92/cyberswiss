from app.tools import registry
from app.tools.httpx_probe.adapter import HttpxProbeAdapter
from app.tools.nuclei.adapter import NucleiAdapter
from app.tools.subfinder.adapter import SubfinderAdapter

registry.register(SubfinderAdapter())
registry.register(HttpxProbeAdapter())
registry.register(NucleiAdapter())
