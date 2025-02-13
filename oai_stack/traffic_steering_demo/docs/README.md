Overview
---

This demo follows the [uplink-classification](https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed/-/blob/master/docs/DEPLOY_SA5G_ULCL.md?ref_type=heads) setup, with simulated OpenAirInterface 5G Core (AMF, PCF, SMF, UPFs, etc) and Gnbsim 5G RAN and UEs, and two data networks (one internet and one edge).

The key is to test the traffic steering policy control using the Service-based inteface (SBI) of the Policy Contorl Function (PCF) to enable the edge access for one UE (e.g., UE2).

Get Started
---

### setup the local PCF image
Since we will be using the SBI of the PCF, we need to have a local PCF image that has more customized SBI endpoints, instead of the official `oaisoftwarealliance/oai-pcf` image. Refer to [LOCAL_PCF_SETUP.md](LOCAL_PCF_SETUP.md) to setup the local PCF docker image.

### setup the local edge container image
Since we will be deploying AI RESE API servers within the edge container, we need to install all the AI server-related dependencies (e.g., fastapi, torch, transformers, pillow etc.) beforehand. Refer to [LOCAL_EDGE_SETUP.md](LOCAL_EDGE_SETUP.md) to setup the local edge docker image.

### setup the local RAN/UE container image
Since we will be running a REST API client from the UE to invoke AI services deployed in the edge container, we need also install some dependencies such as requests. Refer to [LOCAL_RAN_UE_SETUP.md](LOCAL_RAN_UE_SETUP.md) to setup the local RAN/UE docker image.

### pull the remaining docker images
```bash
cd 6G-Pipeline/oai_stack/traffic_steering_demo
docker compose -f docker-compose-core.yaml pull --ignore-pull-failures
```

Note that we added the `--ignore-pull-failures` flag to ignore the pull failures for the images that we have built locally. The rest of the images from oaisoftwarealliance should be pulled successfully.

### start the core network
```bash
cd 6G-Pipeline/oai_stack/traffic_steering_demo
# remove existing containers if any
docker compose -f docker-compose-core.yaml down --remove-orphans
docker compose -f docker-compose-core.yaml up -d
```

<strong>Important</strong> After the start of the core network, wait for at least 20 seconds to ensure all the network functions are intiailized, before starting the RAN and UEs.

<strong>Important</strong> the two sets of UEs have to be started one after another to avoid conflicts caused by currently-unknown issues...

### start the first RAN/UE1
```bash
cd 6G-Pipeline/oai_stack/traffic_steering_demo
docker compose -f docker-compose-ran-ue.yaml up gnbsim-vpp -d
```

Wait for at least 10 seconds before starting the second RAN/UE2.

### start the second RAN/UE2
```bash
cd 6G-Pipeline/oai_stack/traffic_steering_demo
docker compose -f docker-compose-ran-ue.yaml up gnbsim-vpp2 -d
```

### Verify the entire stack
Check the log of UE1 and UE2, and by right, UE1 should have an IP address of `12.1.1.2` and UE2 should have an IP address of `12.1.1.3`. 

```bash
docker exec -it gnbsim-vpp bash
ip a | grep 12.1.1
```


Documentations
---

### Policy Control Function:
* [PCF_SBI.md](PCF_SBI.md) introduces the service-based interface for the Policy Control Function.
* [PCF_POLICY_CONFIG.md](PCF_POLICY_CONFIG.md) explains how to configure the PCF policies for traffic steering.
