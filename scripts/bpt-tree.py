# Дерево шагов БП из dump.json (см. bpt-dump.py): python3 -I scripts/bpt-tree.py dump.json
import sys, json
d = json.load(open(sys.argv[1]))
print("VARIABLES:")
for k, v in d['VARIABLES'].items():
    print(f"  {k}: {v['Name']} [{v['Type']}] mult={v['Multiple']} def={v['Default']!r}")
print("PARAMS:", d['PARAMETERS'])
def walk(n, depth=0):
    if not isinstance(n, dict): return
    ind = '  ' * depth
    props = n.get('Properties', {})
    title = props.get('Title') or n.get('Name')
    print(f"{ind}- {n.get('Type')} | {title} | {n.get('Name')}")
    for k, v in props.items():
        if k in ('Title',): continue
        s = json.dumps(v, ensure_ascii=False)
        if s not in ('""', 'null', '[]', '{}'):
            print(f"{ind}    {k}: {s[:400]}")
    for c in (n.get('Children') or {}).values():
        walk(c, depth + 1)
t = d['TEMPLATE']
for n in (t.values() if all(isinstance(x, dict) for x in t.values()) and 'Type' not in t else [t]):
    walk(n)
