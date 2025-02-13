# Service-based Interface (SBI) of Policy Control Function

Like many other network functions, Policy Control Function exposes its SBI for network operators to interface with it. In OpenAirInterface stack, the SBI of PCF is implemented using http2 REST API server. 

Below is the list of API endpoints that are available in our customized PCF's SBI:

Session Management Policies
---

### Get all SM policies (Added by YUN)

When using the `GET` API on the PCF's SBI, the PCF will only setup the policy configuration for connected UEs. The PCF will not setup the policy for UEs that are not connected even they are listed in the configuration file.

```bash
# only when you're inside any network function contianer, e.g., SMF, AMF, or PCF itself, 
# which has access to the PCF's SBI
curl --http2-prior-knowledge -X GET http://pcf_host:pcf_port/npcf-smpolicycontrol/v1/sm-policies
```

For example:
```bash
curl --http2-prior-knowledge -X GET http://192.168.70.139:8080/npcf-smpolicycontrol/v1/sm-policies
```

For development purpose, in our `docker-compose-core,yaml` file, we've exposed the port `8080` of PCF to the localhost port `13980`, so that we can talk to PCF directly from any application running in our system.

For example, you can use the example python script to get all the SM policies from PCF:

```bash
# install the required dependencies for python script
pip install -U httpx[http2]

cd 6G-Pipeline/oai_stack/traffic_steering_demo/SBI_tester
python pcf.py
```

Example response, in the format of a dictionary with the key being the policy's ID and the value being the SM policy configuration for an UE:

```json
{
    "1": {
        "context": {
            "dnn": "default",
            "notificationUri": "",
            "pduSessionId": 1,
            "pduSessionType": "IPV4",
            "servingNetwork": {
                "mcc": "208",
                "mnc": "95"
            },
            "sliceInfo": {
                "sd": "00007B",
                "sst": 222
            },
            "supi": "imsi-208950000000031"
        },
        "policy": {
            "pccRules": {
                "internet-rule-qos-constrained": {
                    "flowInfos": [
                        {
                            "flowDescription": "permit out ip from any to assigned"
                        }
                    ],
                    "pccRuleId": "internet-rule-qos-constrained",
                    "precedence": 10,
                    "refQosData": [],
                    "refTcData": [
                        "internet-scenario"
                    ]
                }
            },
            "qosDecs": {},
            "traffContDecs": {
                "internet-scenario": {
                    "routeToLocs": [
                        {
                            "dnai": "access"
                        },
                        {
                            "dnai": "ulcl"
                        },
                        {
                            "dnai": "aupf1"
                        },
                        {
                            "dnai": "internet"
                        }
                    ],
                    "tcId": "internet-scenario"
                }
            }
        }
    },
    "2": {
        "context": {
            "dnn": "default",
            "notificationUri": "",
            "pduSessionId": 1,
            "pduSessionType": "IPV4",
            "servingNetwork": {
                "mcc": "208",
                "mnc": "95"
            },
            "sliceInfo": {
                "sd": "00007B",
                "sst": 222
            },
            "supi": "imsi-208950000000032"
        },
        "policy": {
            "pccRules": {
                "internet-rule-qos-unlimited": {
                    "flowInfos": [
                        {
                            "flowDescription": "permit out ip from any to assigned"
                        }
                    ],
                    "pccRuleId": "internet-rule-qos-unlimited",
                    "precedence": 10,
                    "refQosData": [],
                    "refTcData": [
                        "internet-scenario"
                    ]
                }
            },
            "qosDecs": {},
            "traffContDecs": {
                "internet-scenario": {
                    "routeToLocs": [
                        {
                            "dnai": "access"
                        },
                        {
                            "dnai": "ulcl"
                        },
                        {
                            "dnai": "aupf1"
                        },
                        {
                            "dnai": "internet"
                        }
                    ],
                    "tcId": "internet-scenario"
                }
            }
        }
    }
}
```

### Get a single SM policy
```bash
curl --http2-prior-knowledge -X GET http://pcf_host:pcf_port/npcf-smpolicycontrol/v1/sm-policies/1
```

for example:
```bash
curl --http2-prior-knowledge -X GET http://192.168.70.139:8080/npcf-smpolicycontrol/v1/sm-policies/1
```

Below is what it looks like for a single policy `GET` result for one UE with single PCC rule.

```json
{
  "context": {
    "dnn": "default",
    "notificationUri": "",
    "pduSessionId": 1,
    "pduSessionType": "IPV4",
    "servingNetwork": {
      "mcc": "208",
      "mnc": "95"
    },
    "sliceInfo": {
      "sd": "00007B",
      "sst": 222
    },
    "supi": "imsi-208950000000031"
  },
  "policy": {
    "pccRules": {
      "internet-rule-qos-constrained": {
        "flowInfos": [
          {
            "flowDescription": "permit out ip from any to assigned"
          }
        ],
        "pccRuleId": "internet-rule-qos-constrained",
        "precedence": 10,
        "refQosData": [],
        "refTcData": [
          "internet-scenario"
        ]
      }
    },
    "qosDecs": {},
    "traffContDecs": {
      "internet-scenario": {
        "routeToLocs": [
          {
            "dnai": "access"
          },
          {
            "dnai": "ulcl"
          },
          {
            "dnai": "aupf1"
          },
          {
            "dnai": "internet"
          }
        ],
        "tcId": "internet-scenario"
      }
    }
  }
}
```

below is an example for single UE with two PCC rules:

```json
{
  "context": {
    "dnn": "default",
    "notificationUri": "",
    "pduSessionId": 1,
    "pduSessionType": "IPV4",
    "servingNetwork": {
      "mcc": "208",
      "mnc": "95"
    },
    "sliceInfo": {
      "sd": "00007B",
      "sst": 222
    },
    "supi": "imsi-208950000000031"
  },
  "policy": {
    "pccRules": {
      "edge-rule-qos-unlimited": {
        "flowInfos": [
          {
            "flowDescription": "permit out ip from any to assigned"
          }
        ],
        "pccRuleId": "edge-rule-qos-unlimited",
        "precedence": 9,
        "refQosData": [],
        "refTcData": [
          "edge-scenario"
        ]
      },
      "internet-rule-qos-constrained": {
        "flowInfos": [
          {
            "flowDescription": "permit out ip from any to assigned"
          }
        ],
        "pccRuleId": "internet-rule-qos-constrained",
        "precedence": 10,
        "refQosData": [],
        "refTcData": [
          "internet-scenario"
        ]
      }
    },
    "qosDecs": {},
    "traffContDecs": {
      "edge-scenario": {
        "routeToLocs": [
          {
            "dnai": "access"
          },
          {
            "dnai": "ulcl"
          },
          {
            "dnai": "aupf2"
          },
          {
            "dnai": "edge"
          }
        ],
        "tcId": "edge-scenario"
      },
      "internet-scenario": {
        "routeToLocs": [
          {
            "dnai": "access"
          },
          {
            "dnai": "ulcl"
          },
          {
            "dnai": "aupf1"
          },
          {
            "dnai": "internet"
          }
        ],
        "tcId": "internet-scenario"
      }
    }
  }
}
```

Policy Decision Provisioning API
---

Check out the test scripts at [pcf_provisioning_endpoint.py](../SBI_tester//pcf_provisioning_endpoint.py) for GET request examples.

Check out the test scripts at [pcf_provisioning_api_update_ue_access.py](../SBI_tester//pcf_provisioning_api_update_ue_access.py) for PUT request examples.

References
--- 

* https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-pcf/-/merge_requests/29