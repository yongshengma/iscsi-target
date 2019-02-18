def parse_target(lines):
    ### single target
    target = {
        'id': '',
        'name': '',
        'content': {
            'System information': {},
            'I_T nexus information': [],
            'LUN information': [],
            'Account information': [],
            'ACL information': [],
        }
    }
    
    hooks = []
    
    hooks.append(lines.index("System information:"))
    hooks.append(lines.index("I_T nexus information:"))
    hooks.append(lines.index("LUN information:"))
    hooks.append(lines.index("Account information:"))
    hooks.append(lines.index("ACL information:"))
    hooks.append(len(lines))
    
    ### Target id, name
    line = lines[0].split(': ')
    target['id'], target['name'] = (line[0].split(' '))[1], line[1]
    
    ### System information:
    target['content']['System information'] = dict(s.split(': ') for s in lines[hooks[0]+1:hooks[1]])
    
    ### I_T nexus information:
    subhooks = [ lines.index(s) for s in lines[hooks[1]+1:hooks[2]] if 'I_T nexus:' in s ]
    
    z = []
    for idx in subhooks:
        w = []
        w.append(lines[idx])
        g = lines[idx+1].split(' ',2)
        w.append(g[0]+' '+g[1])
        w.append(g[2])
        w.append(lines[idx+2])
        w.append(lines[idx+3])
        z.append(dict( s.split(': ') for s in w ))
    
    target['content']['I_T nexus information'] = z
    
    ### LUN information:
    subhooks = [ lines.index(s) for s in lines[hooks[2]+1:hooks[3]] if 'LUN:' in s ]
    
    z = []
    for idx in subhooks:
        w = []
        w.append(lines[idx])
        w.append(lines[idx+1])
        w.append(lines[idx+2])
        w.append(lines[idx+3])
        g = lines[idx+4].split(', ')
        w.append(g[0])
        w.append(g[1])
        w.append(lines[idx+5])
        w.append(lines[idx+6])
        w.append(lines[idx+7])
        w.append(lines[idx+8])
        w.append(lines[idx+9])
        w.append(lines[idx+10])
        w.append(lines[idx+11])
        w.append(lines[idx+12])
        w.append(lines[idx+13])
        z.append(dict( s.split(': ') for s in w ))
    
    target['content']['LUN information'] = z
    
    
    ### Account information:
    w=[]
    for idx in range(len(lines[hooks[3]+1:hooks[4]])):
        w.append(lines[hooks[3]+1+idx])
    
    target['content']['Account information'] = w
    
    ### ACL information:
    w=[]
    for idx in range(len(lines[hooks[4]+1:hooks[5]])):
        w.append(lines[hooks[4]+1+idx])
    
    target['content']['ACL information'] = w
    
    ### parsing done
    return target

def parse_targets():
    ### all targets
    targets = []
    
    from subprocess import Popen, PIPE
    p = Popen('tgt-admin -s' , shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    
    out = out.split('\n')
    lines = [s.lstrip() for s in out]
    
    tgthooks = [ out.index(s) for s in out if not s.startswith('    ') ]
    
    for idx in range(len(tgthooks) - 1):
        tgt = lines[tgthooks[idx]:tgthooks[idx+1]]
        targets.append(parse_target(tgt))
    
    from pprint import pprint
    pprint(targets)

### main
parse_targets()


