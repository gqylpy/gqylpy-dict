from gqylpy_dict import gdict

data = {
    "_id": "6183aa0a23b60c976c534ac0",
    "timestamp": "2021-11-04T09:38:02.000Z",
    "value": {
        "dimensions": {
            "platform": "MEC",
            "name": "k3sagent-1",
            "uuid": "43F185CF-9AC5-4923-944B-CC8E88D67C23",
            "status": 0,
            "role": "k3s-node",
            "type": "vm",
            "cluster_uuid": "cluster-uuid",
            "datacenter_uuid": "f40a5f86-6195-4348-9c82-5cf859287c4e",
            "collector": "EdgeAgent.KubeNodeInfoCollector"
        },
        "status": "Ready",
        "since": "11d3h15m51s",
        "cause": "The status of k3s node is Ready, it's a vm, and name is k3sagent-1.",
        "ip": "10.121.124.18",
        "ip_internal": "172.16.0.134"
    },
    "tenant_id": "4717c74def42427cac43f1e15628e6f2",
    "region": "useast",
    'list': [
        {'a': 'A'},
        {'b': ['b1', {'b2': 'B2'}]},
        {'': 'kong'},
        {None: 'NONE'}
    ]
}

x = gdict.get_deepvalue(data, 'list[1].b[-1].b3', 'xxx')
print(x)
