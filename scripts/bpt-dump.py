# Разбор экспорта БП Битрикс24 (.bpt): zlib -> сериализованный PHP -> JSON. Код из файла не выполняется.
# Использование: python3 -I scripts/bpt-dump.py файл.bpt > dump.json  (файл копировать в отдельную пустую папку)
import sys, zlib, json

def parse(b, i=0):
    t = chr(b[i])
    if t == 'N':
        return None, i + 2
    if t in 'bid':
        j = b.index(b';', i)
        v = b[i+2:j].decode()
        return (v == '1' if t == 'b' else int(v) if t == 'i' else float(v)), j + 1
    if t == 's':
        j = b.index(b':', i + 2)
        n = int(b[i+2:j])
        s = b[j+2:j+2+n].decode('utf-8', 'replace')
        return s, j + 2 + n + 2
    if t == 'a':
        j = b.index(b':', i + 2)
        n = int(b[i+2:j])
        i = j + 2
        out = {}
        for _ in range(n):
            k, i = parse(b, i)
            v, i = parse(b, i)
            out[k] = v
        return out, i + 1
    raise ValueError('unsupported type %r at %d' % (t, i))

data = zlib.decompress(open(sys.argv[1], 'rb').read())
obj, end = parse(data)
print(json.dumps(obj, ensure_ascii=False, indent=1))
