(function anonymous(Writer, types, util) {
        w = Writer.create()

        if (m.policyType != null && Object.hasOwnProperty.call(m, "policyType"))
            w.uint32(10).string(m.policyType)
        if (m.centralId != null && Object.hasOwnProperty.call(m, "centralId"))
            w.uint32(18).string(m.centralId)
        if (m.province != null && Object.hasOwnProperty.call(m, "province"))
            w.uint32(26).string(m.province)
        if (m.city != null && Object.hasOwnProperty.call(m, "city"))
            w.uint32(34).string(m.city)
        if (m.downtown != null && Object.hasOwnProperty.call(m, "downtown"))
            w.uint32(42).string(m.downtown)
        if (m.garden != null && Object.hasOwnProperty.call(m, "garden"))
            w.uint32(50).string(m.garden)
        if (m.sort != null && Object.hasOwnProperty.call(m, "sort"))
            w.uint32(56).uint32(m.sort)
        if (m.pageNum != null && Object.hasOwnProperty.call(m, "pageNum"))
            w.uint32(64).uint32(m.pageNum)
        if (m.pageSize != null && Object.hasOwnProperty.call(m, "pageSize"))
            w.uint32(72).uint32(m.pageSize)
        return w
    }
)

const protobufjs = require("protobufjs");
const jdata={
    "nested": {
        "PolicyInfoParam": {
            "fields": {
                "id": {
                    "type": "string",
                    "id": 1
                }
            }
        },
        "PolicyInfoByTypeIdParam": {
            "fields": {
                "policyType": {
                    "type": "string",
                    "id": 1
                },
                "centralId": {
                    "type": "string",
                    "id": 2
                },
                "province": {
                    "type": "string",
                    "id": 3
                },
                "city": {
                    "type": "string",
                    "id": 4
                },
                "downtown": {
                    "type": "string",
                    "id": 5
                },
                "garden": {
                    "type": "string",
                    "id": 6
                },
                "sort": {
                    "type": "uint32",
                    "id": 7
                },
                "pageNum": {
                    "type": "uint32",
                    "id": 8
                },
                "pageSize": {
                    "type": "uint32",
                    "id": 9
                }
            }
        },
        "PolicyInfoByTagsIdParam": {
            "fields": {
                "id": {
                    "type": "uint32",
                    "id": 1
                },
                "customerTagId": {
                    "type": "uint32",
                    "id": 2
                },
                "keyword": {
                    "type": "string",
                    "id": 3
                },
                "pageNum": {
                    "type": "uint32",
                    "id": 4
                },
                "pageSize": {
                    "type": "uint32",
                    "id": 5
                }
            }
        },
        "PolicyInfoByDeptIdParam": {
            "fields": {
                "department": {
                    "type": "uint32",
                    "id": 1
                },
                "customized": {
                    "type": "string",
                    "id": 2
                },
                "garden": {
                    "type": "string",
                    "id": 3
                },
                "pageNum": {
                    "type": "uint32",
                    "id": 4
                },
                "pageSize": {
                    "type": "uint32",
                    "id": 5
                }
            }
        },
        "PolicyInfoSearchParam": {
            "fields": {
                "word": {
                    "type": "string",
                    "id": 1
                },
                "department": {
                    "type": "string",
                    "id": 2
                },
                "policyType": {
                    "type": "string",
                    "id": 3
                },
                "industry": {
                    "type": "string",
                    "id": 4
                },
                "customerIndt": {
                    "type": "string",
                    "id": 5
                },
                "startTime": {
                    "type": "string",
                    "id": 6
                },
                "endTime": {
                    "type": "string",
                    "id": 7
                },
                "province": {
                    "type": "string",
                    "id": 8
                },
                "city": {
                    "type": "string",
                    "id": 9
                },
                "downtown": {
                    "type": "string",
                    "id": 10
                },
                "garden": {
                    "type": "string",
                    "id": 11
                },
                "wholews": {
                    "type": "uint32",
                    "id": 12
                },
                "type": {
                    "type": "uint32",
                    "id": 13
                },
                "sorttype": {
                    "type": "uint32",
                    "id": 14
                },
                "pageNum": {
                    "type": "uint32",
                    "id": 15
                },
                "pageSize": {
                    "type": "uint32",
                    "id": 16
                }
            }
        }
    }
}
const root = protobufjs.Root.fromJSON(jdata);
const messageRequest = root.lookupType('PolicyInfoByTypeIdParam');

data={
    "pageNum": 1,
    "pageSize": 7,
    "policyType": '4',
    "province": "",
    "city": "",
    "downtown": "",
    "garden": "",
    "centralId": "",
    "sort": 0
}
bytes_text=messageRequest.encode(data).finish().slice();

console.log(bytes_text);
function getBuffer(policyType){
    data.policyType=policyType;
    return messageRequest.encode(data).finish().slice();
}
console.log(buf2hex(bytes_text));

function buf2hex(buffer) {
   return Array.prototype.map.call(new Uint8Array(buffer), x => ('00' +
         x.toString(16)).slice(-2)).join('');

}
var  uint8Array = Uint8Array.from([10,1,52,18,0,26,0,34,0,42,0,50,0,56,0,64,1,72,7])
 function uint8Array2hex(uint8Array) {
     return Array.prototype.map
       .call(uint8Array, (x) => ('00' + x.toString(16)).slice(-2))
       .join('');
 }

console.log(uint8Array2hex(uint8Array));