import json

def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError as e:
        return str(e)

s = '{"foo": "bar"}'
print(is_valid_json(s))  # returns True

# s = '{"foo": "bar", "baz":}'
# print(is_valid_json(s)) 