#!/usr/bin/env python3
"""
Exact structural enumeration of the first 8-state hidden-phase extension.

Model:
    state sigma_n = (j_n, h_n),  j_n in Z/4, h_n in Z/2
    j_{4n+r} = j_n + EXP[r] mod 4
    h_{4n+r} = h_n xor phi(j_n,r)

with phi(0,0)=0 so leading zero digits fix the initial state (0,0).

State-dependent hidden relabelings
    h -> h xor g(j),  g(0)=0
act by
    phi'(j,r)=phi(j,r) xor g(j) xor g(j+EXP[r]).
They are exact equivalences, giving 32768 / 8 = 4096 gauge classes.

The script computes reachable states and the exact set of adjacent transitions
sigma_n -> sigma_{n+1}; no finite prefix sampling is used.
"""
from collections import Counter

EXP=(0,1,3,0)

def bit(mask,j,r):
    return (mask>>(4*j+r))&1

def step(mask,state,r):
    j,h=state
    return ((j+EXP[r])&3, h^bit(mask,j,r))

def gauge_transform(mask,g):
    out=0
    for j in range(4):
        for r in range(4):
            jp=(j+EXP[r])&3
            b=bit(mask,j,r)^g[j]^g[jp]
            if b:
                out |= 1<<(4*j+r)
    return out

GAUGES=[
    (0,(z>>0)&1,(z>>1)&1,(z>>2)&1)
    for z in range(8)
]

def canonical(mask):
    return min(gauge_transform(mask,g) for g in GAUGES)

def reachable(mask):
    seen={(0,0)}
    todo=[(0,0)]
    while todo:
        s=todo.pop()
        for r in range(4):
            t=step(mask,s,r)
            if t not in seen:
                seen.add(t); todo.append(t)
    return frozenset(seen)

def adjacent_edges(mask):
    """
    Exact carry analysis.

    Write n as prefix, then one digit r<3, then t trailing 3's.
    n+1 has the same prefix, digit r+1, then t trailing 0's.
    For each reachable prefix state and r=0,1,2, iterate the finite pair
    dynamics under (digit3,digit0) until it repeats.
    """
    out=set()
    for pref in reachable(mask):
        for r in range(3):
            a=step(mask,pref,r)
            b=step(mask,pref,r+1)
            seen=set()
            while (a,b) not in seen:
                seen.add((a,b))
                out.add((a,b))
                a=step(mask,a,3)
                b=step(mask,b,0)
    return frozenset(out)

def phi_table(mask):
    return [[bit(mask,j,r) for r in range(4)] for j in range(4)]

def main():
    masks=[m for m in range(1<<16) if (m&1)==0]
    reps={}
    for m in masks:
        c=canonical(m)
        reps[c]=reps.get(c,0)+1

    assert len(masks)==32768
    assert len(reps)==4096
    assert set(reps.values())=={8}

    reach_dist=Counter()
    edge_dist=Counter()
    rows=[]
    for c in sorted(reps):
        rs=reachable(c)
        es=adjacent_edges(c)
        reach_dist[len(rs)]+=1
        edge_dist[len(es)]+=1
        rows.append((len(es),len(rs),c,es))

    assert reach_dist==Counter({8:4095,4:1})
    assert edge_dist[8]==1
    assert edge_dist[16]==1
    assert edge_dist[18]==8

    full=[x for x in rows if x[1]==8]
    min_edges=min(x[0] for x in full)
    mins=[x for x in full if x[0]==min_edges]
    assert min_edges==16
    assert len(mins)==1

    _,_,mask,edges=mins[0]
    assert mask==0x42

    print("HIDDEN-PHASE STRUCTURE PASS")
    print("raw cocycles:",len(masks))
    print("gauge classes:",len(reps))
    print("reachable-state distribution:",dict(sorted(reach_dist.items())))
    print("adjacent-edge distribution:",dict(sorted(edge_dist.items())))
    print("minimum fully-reachable adjacent edges:",min_edges)
    print("unique minimum gauge representative: 0x%04x"%mask)
    print("phi table:")
    for j,row in enumerate(phi_table(mask)):
        print(" ",j,row)
    print("exact adjacent edges:")
    for e in sorted(edges):
        print(" ",e)

if __name__=="__main__":
    main()
