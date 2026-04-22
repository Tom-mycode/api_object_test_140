from jsonpath import jsonpath

data = {
    "code": 0,
    "msg": "success",
    "data": {
        "user": {
            "id": 1001,
            "name": "Tom",
            "roles": ["admin", "tester"],
            "address": {
                "city": "Shanghai",
                "zipcode": "200000"
            }
        }
    }
}

if __name__ == '__main__':
    result1 = jsonpath(data, '$.data.user.name')
    print(result1)
    result2 = jsonpath(data, '$.data.user.roles[*]')
    print(result2)
    result3 = jsonpath(data, '$.data.user.roles[0]')
    print(result3)
    result4 = jsonpath(data, '$.data.user.address')
    print(result4)
    result5 = jsonpath(data, '$..name')
    print(result5)
