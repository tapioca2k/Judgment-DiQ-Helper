import json

# make nodes w/ no connections
'''
nodes = []
i = 0
def make_node(i, t):
    node = {'id': i, 'type': t}
    return node

def save(n):
    j = {'nodes': n}
    js = json.dumps(j)
    with open('judgment.json', 'w') as file:
        file.write(js)


while True:
    t = input('Type: ')
    nodes.append(make_node(i, t))
    i += 1
    save(nodes)
'''

# connect nodes
def save_nodes(nodes):
    j = {'nodes': nodes}
    js = json.dumps(j)
    with open('judgment.json', 'w') as file:
        file.write(js)

with open('judgment.json', 'r') as file:
    j = json.loads(file.read())
    nodes = j['nodes']
for node in nodes:
        connections = input('Node #%s (%s):' % (node['id'], node['type']))
        splits = connections.split(',')
        node['connections'] = splits
        save_nodes(nodes)
