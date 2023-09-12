
with open('viewer_template.html') as f:
    h = f.read()

with open('gsecrets/graph.json') as f:
    jstr = f.read()

out = h.replace('INSERT_DATA_HERE', jstr)

with open('gsecrets/viewer.html', 'w') as f:
    f.write(out)
