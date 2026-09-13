#!/usr/bin/env python3
"""
Exact free-scale rank classification for the four-state tagged-lift family.

Standard library only.

For exact-5 partitions of the eight transition edges, this checker proves:
  * rational step-equality consistency/rank is independent of nonzero A and M>0;
  * 184/1050 partitions are inconsistent;
  * among 866 consistent partitions, 839 have full rank 9 and 27 rank 6;
  * every rank-9 partition is impossible for every admissible free scale
    satisfying v2(N(A)) = v2(M), using only P_(0,4) and P_(3,7).

The rank-9 normalized valuation test is carried out over exact rational
Gaussian numbers, so it does not assume that the fixed-scale A=4 solution is
integral.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction

EXP=(0,1,3,0)
B=((0,0),(1,0),(1,1),(1,0))
UNIT=((1,0),(0,1),(-1,0),(0,-1))
EDGES=((0,1),(0,2),(1,2),(1,3),(2,3),(2,0),(3,0),(3,1))
NVAR=9

def rot4(x,y,s):
    s &= 3
    if s==0: return x,y
    if s==1: return -y,x
    if s==2: return -x,-y
    return y,-x

def triangle_at(n):
    if n==0: return 0,0,0
    digs=[]
    while n:
        digs.append(n&3); n >>= 2
    x=y=s=0
    for r in reversed(digs):
        x*=2; y*=2
        bx,by=rot4(B[r][0],B[r][1],s)
        x+=bx; y+=by
        s=(s+EXP[r])&3
    return x,y,s

def parts(n,k):
    a=[0]*n
    def rec(i,mx):
        if i==n:
            if mx+1==k: yield tuple(a)
            return
        for v in range(min(mx+1,k-1)+1):
            a[i]=v
            yield from rec(i+1,max(mx,v))
    yield from rec(1,0)

def coeff(j,k,off):
    r=[0]*NVAR
    if k: r[off+k-1]+=1
    if j: r[off+j-1]-=1
    return r

# We may compute at the convenient reference scale A=4, M=16 because the
# coefficient matrix is scale-independent and normalized particular solutions
# are obtained by dividing horizontal coordinates by 4.
AFF=[]
for j,k in EDGES:
    ux,uy=UNIT[j]
    AFF.append(((4*ux,coeff(j,k,0)),(4*uy,coeff(j,k,3)),(16,coeff(j,k,6))))

def rows(labels):
    reps={}; out=[]
    for i,l in enumerate(labels):
        if l not in reps:
            reps[l]=i; continue
        r=reps[l]
        for q in range(3):
            ci,vi=AFF[i][q]; cr,vr=AFF[r][q]
            out.append([vi[t]-vr[t] for t in range(NVAR)] + [cr-ci])
    return out

def rref(rs):
    a=[[Fraction(x) for x in r] for r in rs]
    pr=0; piv=[]
    for c in range(NVAR):
        p=next((r for r in range(pr,len(a)) if a[r][c]),None)
        if p is None: continue
        a[pr],a[p]=a[p],a[pr]
        z=a[pr][c]
        a[pr]=[x/z for x in a[pr]]
        for r in range(len(a)):
            if r==pr or not a[r][c]: continue
            z=a[r][c]
            a[r]=[a[r][q]-z*a[pr][q] for q in range(NVAR+1)]
        piv.append(c); pr+=1
    for r in a:
        if all(r[c]==0 for c in range(NVAR)) and r[-1]!=0:
            return False,len(piv),[],[]
    free=[c for c in range(NVAR) if c not in piv]
    p=[Fraction(0)]*NVAR
    for rr,c in enumerate(piv): p[c]=a[rr][-1]
    bas=[]
    for f in free:
        v=[Fraction(0)]*NVAR; v[f]=1
        for rr,c in enumerate(piv): v[c]=-a[rr][f]
        bas.append(v)
    return True,len(piv),p,bas

def v2z(x):
    x=abs(int(x))
    if x==0: return 10**9
    return (x&-x).bit_length()-1

def v2q(x):
    x=Fraction(x)
    if x==0: return 10**9
    return v2z(x.numerator)-v2z(x.denominator)

def normalized_pair(part,m,n):
    # delta = d/A; using reference A=4.
    dx=[Fraction(0)]+[part[i]/4 for i in range(3)]
    dy=[Fraction(0)]+[part[i]/4 for i in range(3,6)]
    # In every rank-9 case the homogeneous height block has unique c=0.
    assert all(part[i]==0 for i in range(6,9))
    zmx,zmy,sm=triangle_at(m); znx,zny,sn=triangle_at(n)
    x=Fraction(znx-zmx)+dx[sn]-dx[sm]
    y=Fraction(zny-zmy)+dy[sn]-dy[sm]
    return v2q(x*x+y*y) == v2z(n-m)


def canon(labels):
    mp={}; nxt=0; out=[]
    for x in labels:
        if x not in mp:
            mp[x]=nxt; nxt+=1
        out.append(mp[x])
    return tuple(out)

def rotate_partition(labels,r):
    out=[None]*8
    for i,l in enumerate(labels):
        out[(i+2*r)%8]=l
    return canon(out)

def orbit_reps(labels_list):
    rem=set(labels_list); reps=[]
    while rem:
        a=min(rem)
        orb={rotate_partition(a,r) for r in range(4)}
        reps.append(a)
        rem-=orb
    return reps

def rank6_common_form(part,basis):
    assert len(basis)==3
    xb=yb=cb=None
    for b in basis:
        sx=any(b[i] for i in range(3))
        sy=any(b[i] for i in range(3,6))
        sc=any(b[i] for i in range(6,9))
        if (sx,sy,sc)==(True,False,False): xb=list(b[:3])
        elif (sx,sy,sc)==(False,True,False): yb=list(b[3:6])
        elif (sx,sy,sc)==(False,False,True): cb=list(b[6:9])
        else: return False
    return (
        xb is not None and xb==yb==cb
        and all(part[i]==0 for i in range(6,9))
    )

def main():
    total=bad=0
    ranks=Counter()
    rank9=[]
    rank6=[]
    for lab in parts(8,5):
        total+=1
        ok,r,p,b=rref(rows(lab))
        if not ok:
            bad+=1
            continue
        ranks[r]+=1
        if r==9:
            rank9.append((lab,p))
        elif r==6:
            rank6.append((lab,p,b))
    assert total==1050
    assert bad==184
    assert ranks==Counter({9:839,6:27}),ranks

    pat=Counter()
    survivors=[]
    for lab,p in rank9:
        a=normalized_pair(p,0,4)
        b=normalized_pair(p,3,7)
        pat[(a,b)]+=1
        if a and b: survivors.append(lab)

    expected=Counter({(False,False):509,(False,True):165,(True,False):165})
    assert pat==expected,(pat,expected)
    assert not survivors
    assert len(rank6)==27
    assert all(rank6_common_form(p,b) for _,p,b in rank6)
    reps=orbit_reps([lab for lab,_,_ in rank6])
    assert len(reps)==8

    print("FREE-SCALE RANK CLASSIFICATION PASS")
    print("exact-5: 1050")
    print("linear inconsistent: 184")
    print("rank 9: 839")
    print("rank 6: 27")
    print("rank-9 P04/P37: both_fail=509 only_P04=165 only_P37=165 survivors=0")
    print("rank-6 common affine form: PASS")
    print("rank-6 C4 rotation orbits: 8")
    print("remaining free-scale search: 27 rank-6 partitions / 8 orbits")

if __name__=="__main__":
    main()
