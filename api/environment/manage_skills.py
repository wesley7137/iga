import json

def add_object_to_json(new_object, filename='api/environment/skills_db.json'):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    data.append(new_object)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

new_object = {
    "name": "newTool",
    "content": {
        "path": "tools.new_tool_path",
        "description": "This is a new tool"
    }
}

# test usage
# add_object_to_json(new_object)
