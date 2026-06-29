import xml.etree.ElementTree as ET
from typing import Any

from app.tools.base import NormalizedResult, ResultType, ToolAdapter


class NmapAdapter(ToolAdapter):
    name = "nmap"

    def build_command(self, params: dict[str, Any]) -> list[str]:
        target = params["target"]
        command = ["nmap", "-oX", "-", "-Pn", "-T4", "--open"]
        ports = params.get("ports")
        if ports:
            command += ["-p", str(ports)]
        command.append(target)
        return command

    def parse_output(self, stdout: str, stderr: str) -> list[NormalizedResult]:
        results = []
        try:
            root = ET.fromstring(stdout)
        except ET.ParseError:
            return results

        for host_el in root.findall("host"):
            address_el = host_el.find("address")
            address = address_el.get("addr") if address_el is not None else None
            if not address:
                continue
            ports_el = host_el.find("ports")
            if ports_el is None:
                continue
            for port_el in ports_el.findall("port"):
                state_el = port_el.find("state")
                if state_el is None or state_el.get("state") != "open":
                    continue
                port_id = port_el.get("portid")
                protocol = port_el.get("protocol")
                service_el = port_el.find("service")
                service = service_el.get("name") if service_el is not None else "unknown"
                results.append(
                    NormalizedResult(
                        type=ResultType.finding,
                        value=f"{address}:{port_id}/{protocol} {service}",
                        raw={
                            "address": address,
                            "port": port_id,
                            "protocol": protocol,
                            "service": service,
                        },
                    )
                )
        return results
