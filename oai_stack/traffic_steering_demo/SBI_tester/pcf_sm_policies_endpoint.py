import httpx
import os
import json

PCF_IP_ADDRESS = os.getenv("PCF_IP_ADDR", "localhost")
PCF_SBI_PORT = os.getenv("PCF_SBI_PORT", 13980)

sm_policies_base_url = f"http://{PCF_IP_ADDRESS}:{PCF_SBI_PORT}/npcf-smpolicycontrol/v1/sm-policies"


def send_get_request(url):
    with httpx.Client(http2=True, http1=False) as client:
        response = client.get(url)
        return json.loads(response.text)

# Sending an HTTP/2 GET request
print("---------- GET all SM policies ------------")
print(sm_policies_base_url)
sm_policies = send_get_request(sm_policies_base_url)
print(json.dumps(sm_policies, indent=4))
    
if len(sm_policies) == 0:
    print("PCF has not created any sm policies yet. Make sure you have started at least one UE.")
    exit(0)
    
print("\n---------- GET a single SM policy ------------")
single_sm_policy_url = f"{sm_policies_base_url}/1"
print(single_sm_policy_url)
single_sm_policy = send_get_request(single_sm_policy_url)
print(json.dumps(single_sm_policy, indent=4))
