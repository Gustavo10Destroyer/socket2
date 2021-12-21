import json
import base64

def dumps(data, string: bool = True):
  if type(data) in [list, tuple]:
    output = []

    for element in data:
      key = data.index(element)

      if type(element) == complex:
        output.append("complex:" + str(element))
      elif type(element) in [int, float, bool]:
        output.append(element)
      elif type(element) == str:
        output.append("str:" + base64.b64encode(element.encode()).decode())
      elif type(element) == bytes:
        output.append("bytes:" + base64.b64encode(element).decode())
      elif type(element) in [list, dict]:
        output.append(dumps(element, False))
      elif type(element) == tuple:
        output.append("tuple:" + dumps(element))

    if string:
      return json.dumps(output)
    else:
      return output
  elif type(data) == dict:
    output = {}

    for key in data:
      value = data[key]

      if type(key) == str:
        key = "str:" + base64.b64encode(key.encode()).decode()
      elif type(key) == bytes:
        key = "bytes:" + base64.b64encode(key).decode()
      elif type(key) == complex:
        key = "complex:" + str(key)
      elif type(key) == tuple:
        key = "tuple:" + dumps(key)

      if type(value) == complex:
        output[key] = "complex:" + str(value)
      elif type(value) == bytes:
        output[key] = "bytes:" + base64.b64encode(value).decode()
      elif type(value) in [int, float, bool]:
        output[key] = value
      elif type(value) == str:
        output[key] = "str:" + base64.b64encode(value.encode()).decode()
      elif type(value) in [list, dict]:
        output[key] = dumps(value, False)
      elif type(value) == tuple:
        output[key] = "tuple:" + dumps(value)

    if string:
      return json.dumps(output)
    else:
      return output

def loads(data, string=True):
  if string:
    data = json.loads(data)

  if type(data) == list:
    for element in data:
      key = data.index(element)

      if type(element) == str:
        if element.startswith("complex:"):
          data[key] = complex(element[8:])
        elif element.startswith("bytes:"):
          data[key] = base64.b64decode(element[6:].encode())
        elif element.startswith("str:"):
          data[key] = base64.b64decode(element[4:].encode()).decode()
        elif element.startswith("tuple:"):
          data[key] = tuple(loads(element[6:], False))
      elif type(element) in [list, dict]:
        data[key] = loads(element, False)
    
    return data
  elif type(data) == dict:
    output = {}
    
    for key in data:
      value = data[key]
      
      if type(key) == str:
        if key.startswith("complex:"):
          key = complex(key[8:])
        elif key.startswith("bytes:"):
          key = base64.b64decode(key[6:].encode())
        elif key.startswith("str:"):
          key = base64.b64decode(key[4:].encode()).decode()
        elif key.startswith("tuple:"):
          key = tuple(loads(key[6:], False))
      
      if type(value) == str:
        if value.startswith("complex:"):
          output[key] = complex(value[8:])
        elif value.startswith("bytes:"):
          output[key] = base64.b64decode(value[6:].encode())
        elif value.startswith("str:"):
          output[key] = base64.b64decode(value[4:].encode()).decode()
        elif value.startswith("tuple:"):
          output[key] = tuple(loads(value[6:], False))
      elif type(value) in [list, dict]:
        output[key] = loads(value, False)
      else:
        output[key] = value
    
    return output