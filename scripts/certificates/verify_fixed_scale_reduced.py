#!/usr/bin/env python3
"""Independent standard-library checker for the fixed A=4,M=16 <=5 theorem."""
from __future__ import annotations
from fractions import Fraction as F
from collections import Counter
from itertools import product
import argparse,json,math,time
from pathlib import Path

EXP=(0,1,3,0); B=((0,0),(1,0),(1,1),(1,0)); U=((1,0),(0,1),(-1,0),(0,-1))
E=((0,1),(0,2),(1,2),(1,3),(2,3),(2,0),(3,0),(3,1))
NV=9; CB=30; R9=((0,4),(3,7)); R6=((2,4),(1,5),(1,3),(0,4))

def tri(n):
    ds=[]; t=n
    while t: ds.append(t&3); t>>=2
    x=y=s=0
    for r in reversed(ds):
        x*=2;y*=2
        bx,by=B[r]
        if s==1: bx,by=-by,bx
        elif s==2: bx,by=-bx,-by
        elif s==3: bx,by=by,-bx
        x+=bx;y+=by;s=(s+EXP[r])&3
    return x,y,s

def parts(n,k):
    a=[0]*n
    def rec(i,m):
        if i==n:
            if m+1==k: yield tuple(a)
            return
        for v in range(min(m+1,k-1)+1):
            a[i]=v; yield from rec(i+1,max(m,v))
    yield from rec(1,0)

def canon(a):
    d={}; out=[]
    for x in a:
        if x not in d:d[x]=len(d)
        out.append(d[x])
    return tuple(out)

def rot(p,r):
    a=[0]*8
    for i,x in enumerate(p):a[(i+2*r)%8]=x
    return canon(a)

def orbit_reps(ps):
    rem=set(ps); out=[]
    while rem:
        q=min(rem); o={rot(q,r) for r in range(4)}
        out.append((q,len(o),len(o&rem))); rem-=o
    return out

def refines(f,c):
    return all(f[i]!=f[j] or c[i]==c[j] for i in range(8) for j in range(8))

def tc(j,k,o):
    a=[0]*NV
    if k:a[o+k-1]+=1
    if j:a[o+j-1]-=1
    return a

AFF=[]
for j,k in E:
    ux,uy=U[j]
    AFF.append(((4*ux,tc(j,k,0)),(4*uy,tc(j,k,3)),(16,tc(j,k,6))))

def rows(p):
    rep={}; out=[]
    for i,z in enumerate(p):
        if z not in rep:rep[z]=i;continue
        r=rep[z]
        for c in range(3):
            ci,vi=AFF[i][c]; cr,vr=AFF[r][c]
            out.append([vi[t]-vr[t] for t in range(NV)]+[cr-ci])
    return out

def rref(rs):
    m=[[F(x) for x in r] for r in rs]; pr=0; piv=[]
    for c in range(NV):
        q=next((r for r in range(pr,len(m)) if m[r][c]),None)
        if q is None:continue
        m[pr],m[q]=m[q],m[pr]; z=m[pr][c]; m[pr]=[x/z for x in m[pr]]
        for r in range(len(m)):
            if r!=pr and m[r][c]:
                z=m[r][c];m[r]=[m[r][j]-z*m[pr][j] for j in range(NV+1)]
        piv.append(c);pr+=1
    if any(all(r[c]==0 for c in range(NV)) and r[-1] for r in m): return False,len(piv),[],[]
    free=[c for c in range(NV) if c not in piv]
    p=[F(0)]*NV
    for r,c in enumerate(piv):p[c]=m[r][-1]
    bs=[]
    for f in free:
        v=[F(0)]*NV;v[f]=1
        for r,c in enumerate(piv):v[c]=-m[r][f]
        bs.append(v)
    return True,len(piv),p,bs

def v2(x):
    x=abs(int(x))
    return 10**9 if x==0 else (x&-x).bit_length()-1

def pair_unique(v,m,n):
    dx=[0]+v[:3];dy=[0]+v[3:6];c=[0]+v[6:9]
    ax,ay,a=tri(m);bx,by,b=tri(n)
    x=4*(bx-ax)+dx[b]-dx[a]; y=4*(by-ay)+dy[b]-dy[a]
    h=16*(n-m)+c[b]-c[a]
    return v2(x*x+y*y)==v2(h)

def rank6_form(p,bs):
    xb=yb=cb=None
    for b in bs:
        q=(any(b[:3]),any(b[3:6]),any(b[6:9]))
        if q==(1,0,0):xb=list(b[:3])
        elif q==(0,1,0):yb=list(b[3:6])
        elif q==(0,0,1):cb=list(b[6:9])
        else:raise AssertionError(q)
    assert xb==yb==cb and not any(p[6:9])
    return list(p[:3]),list(p[3:6]),list(p[6:9]),xb

def lcm(a,b):return abs(a*b)//math.gcd(a,b)
def residues(p,v):
    d=1
    for x in list(p)+list(v):d=lcm(d,x.denominator)
    out=set()
    for t in range(16*d):
        z=[p[i]+t*v[i] for i in range(3)]
        if all(x.denominator==1 for x in z):out.add(tuple(int(x)%16 for x in z))
    return sorted(out)

def heights(p,v):
    out=[]
    for t in range(-CB,CB+1):
        z=[p[i]+t*v[i] for i in range(3)]
        if not all(x.denominator==1 for x in z):continue
        c=(0,)+tuple(map(int,z))
        if any(abs(x)>CB for x in c):continue
        if any(16+c[k]-c[j]<1 for j,k in E):continue
        out.append(c)
    return out

def nvmod(x,y):
    def cv(a):
        a%=16
        return 4 if a==0 else v2(a)
    a,b=cv(x),cv(y)
    if a>=4 and b>=4:return 8
    return 2*a+1 if a==b else 2*min(a,b)

def pair_res(x,y,c,m,n):
    X=[0]+list(x);Y=[0]+list(y);ax,ay,a=tri(m);bx,by,b=tri(n)
    dx=(4*(bx-ax)+X[b]-X[a])%16;dy=(4*(by-ay)+Y[b]-Y[a])%16
    h=16*(n-m)+c[b]-c[a];assert 0<h<256
    return nvmod(dx,dy)==v2(h)

def prove():
    P=list(parts(8,5)); assert len(P)==1050
    bad=[]; rec=[]
    for q in P:
        ok,r,p,b=rref(rows(q))
        (rec if ok else bad).append((q,r,p,b) if ok else q)
    assert len(bad)==184 and Counter(r for _,r,_,_ in rec)==Counter({9:839,6:27})
    bad6=[q for q in parts(8,6) if not rref(rows(q))[0]];assert len(bad6)==8
    inh=[q for q in bad if any(refines(z,q) for z in bad6)]
    new=[q for q in bad if q not in set(inh)]
    assert (len(inh),len(new),len(orbit_reps(bad6)),len(orbit_reps(new)))==(114,70,2,20)
    nonint=0; ints=[]
    for q,r,p,b in rec:
        if r!=9:continue
        assert not b
        if any(x.denominator!=1 for x in p):nonint+=1;continue
        z=list(map(int,p));c=[0]+z[6:9]
        assert all(abs(x)<=CB for x in c)
        assert all(16+c[k]-c[j]>=1 for j,k in E)
        ints.append((q,z))
    assert nonint==164 and len(ints)==675
    pat=Counter((pair_unique(z,0,4),pair_unique(z,3,7)) for _,z in ints)
    assert pat==Counter({(False,False):397,(False,True):139,(True,False):139})
    r6=[x for x in rec if x[1]==6];assert len(r6)==27 and len(orbit_reps([x[0] for x in r6]))==8
    progress={}
    for q,_,p,b in r6:
        px,py,pc,v=rank6_form(p,b);xs=residues(px,v);ys=residues(py,v);cs=heights(pc,v)
        assert len(xs)==len(ys)==16
        alive=list(product(xs,ys,cs)); a=[len(alive)]
        for pair in R6:
            alive=[z for z in alive if pair_res(*z,*pair)];a.append(len(alive))
        assert not alive;progress[''.join(map(str,q))]=a
    return {
      "status":"PASS","accounting":{"linear":184,"rank9_nonintegral":164,"rank9_pair_killed":675,"rank6":27,"total":1050},
      "linear":{"bad6":8,"bad6_orbits":2,"inherited5":114,"new5":70,"new5_orbits":20,"types":22},
      "rank9":{"pairs":R9,"pattern":{"both_fail":397,"only_P04":139,"only_P37":139,"survivors":0}},
      "rank6":{"partitions":27,"orbits":8,"pairs":R6,"modulus":16,"survivors":0,"progress":progress}
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--linear-json",type=Path);ap.add_argument("--out",type=Path)
    a=ap.parse_args();t=time.perf_counter();r=prove()
    if a.linear_json:
        old=json.loads(a.linear_json.read_text());actual={q for q in parts(8,5) if not rref(rows(q))[0]}
        assert old["count"]==184 and actual=={tuple(x) for x in old["partitions"]}
        r["linear_crosscheck"]=True
    r["seconds"]=time.perf_counter()-t
    text=json.dumps(r,indent=2)
    print("REDUCED CERTIFICATE PASS");print("1050 = 184 + 164 + 675 + 27");print(text)
    if a.out:a.out.write_text(text+"\n")
if __name__=="__main__":main()
