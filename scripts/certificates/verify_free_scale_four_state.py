#!/usr/bin/env python3
"""
Exact certificate for the free-scale four-state valuation-certified tagged-lift
family in Erdős Problem 193.

Standard library only.

Family:
    W_n = A Z_n + d_{j_n}
    H_n = M n   + c_{j_n}

where A is a nonzero Gaussian integer, M>0, d_j are Gaussian-integer tags,
c_j are integer tags, adjacent height increments are positive, and the
construction is required to satisfy the pairwise valuation certificate

    v2(|W_n-W_m|^2) = v2(H_n-H_m)        for every m<n.

The checker proves that <=5 distinct adjacent step vectors are impossible in
this family for every A,M. Since the audited 6-step construction belongs to
the family, 6 is optimal inside this valuation-certified four-state family.

The result is NOT a global lower bound for Erdős Problem 193 and does not rule
out a four-state tagged lift whose non-collinearity is proved by some different
mechanism.
"""
from __future__ import annotations

from collections import Counter, defaultdict
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

def partitions(n,k):
    a=[0]*n
    def rec(i,mx):
        if i==n:
            if mx+1==k: yield tuple(a)
            return
        for z in range(min(mx+1,k-1)+1):
            a[i]=z
            yield from rec(i+1,max(mx,z))
    yield from rec(1,0)

def coeff(j,k,off):
    r=[0]*NVAR
    if k: r[off+k-1]+=1
    if j: r[off+j-1]-=1
    return r

# Reference scale used only to recover normalized rational solutions.
# Rank/consistency are scale-independent.
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
        u=[Fraction(0)]*NVAR; u[f]=1
        for rr,c in enumerate(piv): u[c]=-a[rr][f]
        bas.append(u)
    return True,len(piv),p,bas

def v2z(x):
    x=abs(int(x))
    if x==0: return 10**9
    return (x&-x).bit_length()-1

def v2q(x):
    x=Fraction(x)
    if x==0: return 10**9
    return v2z(x.numerator)-v2z(x.denominator)

def norm_v2(z):
    x,y=z
    return v2q(x*x+y*y)

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

def orbit_rep(labels):
    return min(rotate_partition(labels,r) for r in range(4))

def rank6_form(part,basis):
    xb=yb=cb=None
    for b in basis:
        sx=any(b[i] for i in range(3))
        sy=any(b[i] for i in range(3,6))
        sc=any(b[i] for i in range(6,9))
        if (sx,sy,sc)==(True,False,False): xb=list(b[:3])
        elif (sx,sy,sc)==(False,True,False): yb=list(b[3:6])
        elif (sx,sy,sc)==(False,False,True): cb=list(b[6:9])
        else: raise AssertionError("unexpected mixed nullspace vector")
    assert xb is not None and xb==yb==cb
    assert all(part[i]==0 for i in range(6,9))
    delta=[(part[i]/4,part[i+3]/4) for i in range(3)]
    return [(Fraction(0),Fraction(0))]+delta,[Fraction(0)]+xb

def pair_triple(delta,v,m,n):
    zmx,zmy,sm=triangle_at(m); znx,zny,sn=triangle_at(n)
    r=(Fraction(znx-zmx)+delta[sn][0]-delta[sm][0],
       Fraction(zny-zmy)+delta[sn][1]-delta[sm][1])
    q=v[sn]-v[sm]
    t=Fraction(n-m)
    return r,q,t

def rank9_pair_ok(part,m,n):
    assert all(part[i]==0 for i in range(6,9))
    delta=[(Fraction(0),Fraction(0))]
    delta += [(part[i]/4,part[i+3]/4) for i in range(3)]
    r,_,t=pair_triple(delta,[Fraction(0)]*4,m,n)
    return norm_v2(r)==v2q(t)

def scalar_multiple(a,b):
    r1,q1,t1=a; r2,q2,t2=b
    s=t2/t1
    return r2[0]==s*r1[0] and r2[1]==s*r1[1] and q2==s*q1, s

def rank6_orbit_certificate(rep,part,basis):
    delta,v=rank6_form(part,basis)
    triples={}
    for m in range(8):
        for n in range(m+1,8):
            triples[(m,n)]=pair_triple(delta,v,m,n)

    # Type A: q=0, so both free parameters disappear. N1 cancels the
    # common A/M scale and leaves norm_v2(R)=v2(t).
    for pair,(r,q,t) in triples.items():
        if q==0 and norm_v2(r)!=v2q(t):
            return {
                "kind":"fixed_pair_mismatch",
                "pair":pair,
                "lhs":norm_v2(r),
                "rhs":v2q(t),
            }

    # Type B: two complete normalized displacement triples differ by an even
    # rational factor s. Then actual horizontal norm valuation shifts by
    # 2*v2(s), while height valuation shifts by only v2(s), so the two pair
    # identities cannot both hold when v2(s)!=0.
    items=list(triples.items())
    for i in range(len(items)):
        p1,a=items[i]
        for j in range(i+1,len(items)):
            p2,b=items[j]
            ok,s=scalar_multiple(a,b)
            if ok and v2q(s)!=0:
                return {
                    "kind":"scalar_pair_mismatch",
                    "pair1":p1,
                    "pair2":p2,
                    "scale":str(s),
                    "v2_scale":v2q(s),
                }

    raise AssertionError(f"no rank-6 certificate for orbit {rep}")

def main():
    total=linear_bad=0
    rank9=[]; rank6=[]
    ranks=Counter()

    for lab in partitions(8,5):
        total+=1
        ok,r,p,b=rref(rows(lab))
        if not ok:
            linear_bad+=1
            continue
        ranks[r]+=1
        if r==9: rank9.append((lab,p))
        elif r==6: rank6.append((lab,p,b))
        else: raise AssertionError(f"unexpected rank {r}")

    assert total==1050
    assert linear_bad==184
    assert ranks==Counter({9:839,6:27})

    pattern=Counter()
    for lab,p in rank9:
        p04=rank9_pair_ok(p,0,4)
        p37=rank9_pair_ok(p,3,7)
        pattern[(p04,p37)]+=1
    assert pattern==Counter({
        (False,False):509,
        (False,True):165,
        (True,False):165,
    })

    byrep=defaultdict(list)
    for row in rank6:
        byrep[orbit_rep(row[0])].append(row)
    assert len(byrep)==8

    certs={}
    covered=0
    for rep,members in sorted(byrep.items()):
        witness=next(x for x in members if x[0]==rep)
        cert=rank6_orbit_certificate(rep,witness[1],witness[2])
        certs[rep]=cert
        covered += len(members)

    assert covered==27

    fixed=sum(c["kind"]=="fixed_pair_mismatch" for c in certs.values())
    scalar=sum(c["kind"]=="scalar_pair_mismatch" for c in certs.values())
    assert fixed+scalar==8

    print("FREE-SCALE FOUR-STATE <=5 CERTIFICATE PASS")
    print("scope: valuation-certified four-state tagged lifts")
    print("exact-5 partitions: 1050")
    print("linear inconsistent: 184")
    print("rank 9 eliminated: 839")
    print("  P04/P37 both_fail=509 only_P04=165 only_P37=165 survivors=0")
    print("rank 6 eliminated: 27 in 8 C4 orbits")
    print(f"  orbit certificates: fixed_pair={fixed} scalar_pair={scalar}")
    for rep,c in sorted(certs.items()):
        print(" ", "".join(map(str,rep)), c)
    print("survivors: 0")
    print("conclusion: >=6 steps in this free-scale valuation-certified family")

if __name__=="__main__":
    main()
