import httpx
import os
import json
import subprocess
from typing import Literal

PCF_IP_ADDRESS = os.getenv("PCF_IP_ADDR", "localhost")
PCF_SBI_PORT = os.getenv("PCF_SBI_PORT", 13980)

provisioning_base_url = f"http://{PCF_IP_ADDRESS}:{PCF_SBI_PORT}/npcf-provisioning/v1"

def send_http2_to_pcf(url: str, method: Literal["GET", "PUT"], data=None, restart=False):
    validate_method(method)
    with httpx.Client(http2=True, http1=False) as client:
        response = client.get(url) if method == "GET" else client.put(url, json=data)
        print(response)
        if response is None or response.status_code != 200:
            return None
        if response is not None and response.text is not None and response.text.strip() != "":
            if(method == "PUT" and restart):
                restart_ran(url.split("/")[-1])
            return json.loads(response.text.strip())
        else:
            return None
    
def validate_method(method: str):
    if(method == "GET"):
        return
    elif(method == "PUT"):
        return
    else:
        raise Exception(f"Argument method {method} is unsupported")
        
def restart_ran(UE_supi: str):
    UE = "gnbsim-vpp2" if UE_supi.endswith("32") else "gnbsim-vpp" if UE_supi.endswith("31") else None
    if UE:
        subprocess.run(["./oai_stack/traffic_steering_demo/scripts/linux/restart_ran.sh", UE])



UE_supi = "imsi-208950000000032"
url = f"{provisioning_base_url}/supiPolicyDecision/{UE_supi}"

print("\n---------- GET supiPolicyDecision for UE2 ------------")
print(url)
res = send_http2_to_pcf(url, "GET")
print(res)

print("\n---------- PUT supiPolicyDecision for UE2 ------------")
data = {
    "supi": UE_supi,
    "pccRuleIds": ["edge-rule", "internet-rule"]
}
print(url)
print(json.dumps(data))
res = send_http2_to_pcf(url, "PUT", data = data, restart = False)
print(res)

