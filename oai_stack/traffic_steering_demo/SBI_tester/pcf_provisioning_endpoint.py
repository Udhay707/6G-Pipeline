import httpx
import os
import json

PCF_IP_ADDRESS = os.getenv("PCF_IP_ADDR", "localhost")
PCF_SBI_PORT = os.getenv("PCF_SBI_PORT", 13980)

provisioning_base_url = f"http://{PCF_IP_ADDRESS}:{PCF_SBI_PORT}/npcf-provisioning/v1"


def http2_get_json(url):
    with httpx.Client(http2=True, http1=False) as client:
        response = client.get(url)
        # print(response.text)
        print(response)
        if response is None or response.status_code != 200:
            return None
        if response is not None and response.text is not None and response.text.strip() != "":
            return json.loads(response.text.strip())
        else:
            return None
        
# Sending an HTTP/2 GET request
print("---------- GET defaultDecision ------------")
url = f"{provisioning_base_url}/defaultDecision"
print(url)
res = http2_get_json(url)
print(res)

print("\n---------- GET dnnPolicyDecisions ------------")
url = f"{provisioning_base_url}/dnnPolicyDecisions"
print(url)
res = http2_get_json(url)
print(res)

print("\n---------- GET slicePolicyDecisions ------------")
url = f"{provisioning_base_url}/slicePolicyDecisions"
print(url)
res = http2_get_json(url)
print(res)

print("---------- GET pccRules ------------")
url = f"{provisioning_base_url}/pccRules"
print(url)
res = http2_get_json(url)
print(res)

print("\n---------- GET supiPolicyDecisions ------------")
url = f"{provisioning_base_url}/supiPolicyDecisions"
print(url)
res = http2_get_json(url)
print(res)


