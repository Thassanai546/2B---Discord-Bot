from replit import db
import re

def parse(msg):
  regex = re.compile(r"'[^']*'")
  myList = (regex.findall(msg.strip("!add ")))
  if len(myList) == 2:
    add_weapon(myList[0].strip("'"),myList[1].strip("'"))
    return True
  else:
    return False

def add_weapon(name, desc):
  if name not in db:
    db[name] = desc

def get_weapon(name):
  return db.get(name)

def search_weapons(name):
  match_keys = db.prefix(name)
  return {k: db[k] for k in match_keys}

def delete_weapon(name):
  if name in db:
    del db[name]
    return True
  else:
    return False

def list_weapons():
# Return all weapons, responding status is not a weapon
  result = []
  for key in db.keys():
    if key != "responding":
      result.append(key)
  result.sort()
  return result

def list_all():
  return db.keys()

def set_responding(status):
  db["responding"] = status