#!/usr/bin/env python3
"""Exact HS2 necessary-condition sieve for hidden cocycle phi=0x0042.

The --max-n bound is only a finite search range for exact obstruction witnesses.
A survivor is NOT a construction and NOT proof of all-pair compatibility.
"""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, json, math, platform, subprocess, sys, time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

EXPECTED_N=59254
EXPECTED_RANKS=Counter({(21,0):59135,(18,3):119})
EXPECTED_HASH="6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b"
EXP=(0,1,3,0); B=((0,0),(1,0),(1,1),(1,0))

def load(path,name):
    sp=importlib.util.spec_from_file_location(name,path)
    if sp is None or sp.loader is None: raise RuntimeError(path)
    m=importlib.util.module_from_spec(sp); sys.modules[name]=m; sp.loader.exec_module(m); return m

def hs1mod(): return load(Path(__file__).with_name("search_hs1_linear_partitions.py"),"hs1_hs2")
def hs0mod(): return load(Path(__file__).with_name("enumerate_binary_cocycles.py"),"hs0_hs2")

def rot(x,y,s):
    return ((x,y),(-y,x),(-x,-y),(y,-x))[s&3]

def triangle(n):
    if n==0:return 0,0,0
    ds=[]
    while n: ds.append(n&3); n>>=2
    x=y=j=0
    for r in reversed(ds):
        x*=2;y*=2; bx,by=rot(*B[r],j); x+=bx;y+=by;j=(j+EXP[r])&3
    return x,y,j

def digits(n):
    a=[]
    while n:a.append(n&3);n>>=2
    return reversed(a)

def hstate(n,hs0,hs1):
    s=(0,0)
    for r in digits(n): s=hs0.step(hs1.HIDDEN_PHI,s,r)
    return hs1.HIDDEN_STATE_ID[s]

def v2(x):
    x=F(x)
    if not x:return None
    def z(a): a=abs(a); return (a&-a).bit_length()-1
    return z(x.numerator)-z(x.denominator)

def nv2(r): return v2(r[0]*r[0]+r[1]*r[1])
def vt(x): return "inf" if x is None else str(x)

def unpack(p,b,nstate):
    w=nstate-1
    d=[(F(0),F(0))]+[(F(p[i]),F(p[w+i])) for i in range(w)]
    g=[F(0)]+[F(p[2*w+i]) for i in range(w)]
    if not b:return d,g,None
    if len(b)!=3: raise AssertionError(("nullity",len(b)))
    parts={}
    for u in b:
        hit=[]
        for k in range(3):
            q=tuple(F(x) for x in u[k*w:(k+1)*w])
            if any(q): hit.append((k,q))
        if len(hit)!=1: raise AssertionError("mixed null vector")
        parts[hit[0][0]]=hit[0][1]
    if set(parts)!={0,1,2} or not(parts[0]==parts[1]==parts[2]): raise AssertionError("null blocks differ")
    return d,g,[F(0)]+list(parts[0])

def positive(edges,g,v):
    lo=hi=None
    for ei,(s,t) in enumerate(edges):
        a=F(1)+g[t]-g[s]; q=F(0) if v is None else v[t]-v[s]
        if not q:
            if a<=0:return False,{"kind":"positive_height_infeasible","edge":ei,"a":str(a)}
        else:
            b=-a/q
            if q>0: lo=b if lo is None or b>lo else lo
            else: hi=b if hi is None or b<hi else hi
    if lo is not None and hi is not None and not lo<hi:
        return False,{"kind":"positive_height_infeasible","lower":str(lo),"upper":str(hi)}
    return True,{"lower":None if lo is None else str(lo),"upper":None if hi is None else str(hi)}

def pair_bases(maxn,state_at):
    z=[];s=[]
    for n in range(maxn+1):
        x,y,_=triangle(n);z.append((x,y));s.append(state_at(n))
    return [(m,n,z[n][0]-z[m][0],z[n][1]-z[m][1],s[m],s[n]) for n in range(1,maxn+1) for m in range(n)]

def triple(a,d,g,v):
    m,n,x,y,sm,sn=a
    r=(F(x)+d[sn][0]-d[sm][0],F(y)+d[sn][1]-d[sm][1])
    q=F(0) if v is None else v[sn]-v[sm]
    t=F(n-m)+g[sn]-g[sm]
    return (m,n),r,q,t

def direct(pb,d,g):
    for a in pb:
        p,r,_,t=triple(a,d,g,None);L,R=nv2(r),v2(t)
        if L!=R:return {"kind":"direct_pair_mismatch","pair":list(p),"lhs":vt(L),"rhs":vt(R),"r":[str(r[0]),str(r[1])],"t":str(t)}

def fixed(pb,d,g,v):
    for a in pb:
        p,r,q,t=triple(a,d,g,v)
        if q:continue
        L,R=nv2(r),v2(t)
        if L!=R:return {"kind":"fixed_pair_mismatch","pair":list(p),"lhs":vt(L),"rhs":vt(R)}

def proj(vec):
    vec=tuple(F(x) for x in vec)
    if not any(vec):return None
    den=1
    for x in vec:den=math.lcm(den,x.denominator)
    a=[x.numerator*(den//x.denominator) for x in vec]; gg=0
    for x in a:gg=math.gcd(gg,abs(x))
    a=[x//gg for x in a]
    if next(x for x in a if x)<0:a=[-x for x in a]
    sig=tuple(a); i=next(i for i,x in enumerate(sig) if x); return sig,v2(vec[i]/sig[i])

def scalar(pb,d,g,v):
    seen={}
    for a in pb:
        p,r,q,t=triple(a,d,g,v); P=proj((r[0],r[1],q,t))
        if P is None:continue
        sig,k=P
        if sig in seen and seen[sig][1]!=k:
            p0,k0=seen[sig]; return {"kind":"scalar_pair_mismatch","pair1":list(p0),"pair2":list(p),"v2_scale_ratio":k-k0}
        seen.setdefault(sig,(p,k))

def affine(pb,d,g,v): return fixed(pb,d,g,v) or scalar(pb,d,g,v)

def record_bytes(x): return (json.dumps(x,sort_keys=True,separators=(",",":"))+"\n").encode()

def four_regression(hs1):
    r=hs1.PartitionSearch("four_hs2",hs1.FOUR_STATES,hs1.FOUR_EDGES,output_record_limit=2000).run()
    assert r.feasible_count==866 and r.rank_distribution==Counter({(9,0):839,(6,3):27})
    # The five non-representative rank-6 partitions need witnesses as late as
    # n=31.  Keep this finite regression broader than the first eight points;
    # it does not change the HS2 search horizon or its mathematical scope.
    tab=hs1.equality_row_table(hs1.FOUR_EDGES,hs1.FOUR_STATES); pb=pair_bases(31,lambda n:triangle(n)[2]); c=Counter()
    for lab,er in r.feasible_records:
        ok,rank,p,b=hs1.exact_rref(hs1.rows_for_partition(lab,tab),9); assert ok and rank==er
        d,g,v=unpack(p,b,4); w=direct(pb,d,g) if rank==9 else affine(pb,d,g,v); assert w is not None
        c[rank]+=1
    assert c==Counter({9:839,6:27})

def selftest():
    hs1=hs1mod();hs0=hs0mod();hs1.run_self_tests()
    assert hstate(0,hs0,hs1)==hstate(3,hs0,hs1)==hs1.HIDDEN_STATE_ID[(0,0)]
    z0=triangle(0);z3=triangle(3);assert nv2((F(z3[0]-z0[0]),F(z3[1]-z0[1])))==v2(F(3))==0
    assert proj((F(1),F(2),F(3),F(4)))[0]==proj((F(-2),F(-4),F(-6),F(-8)))[0]
    four_regression(hs1);print("HS2 NORMALIZED VALUATION SELF-TEST PASS")

def gitsha(root):return subprocess.run(["git","rev-parse","HEAD"],cwd=root,check=True,capture_output=True,text=True).stdout.strip()

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--self-test",action="store_true");ap.add_argument("--max-n",type=int,default=127);ap.add_argument("--output-dir",type=Path);a=ap.parse_args()
    if a.self_test:selftest();return 0
    if a.max_n<7:ap.error("--max-n must be >=7")
    hs1=hs1mod();hs0=hs0mod();hs1.assert_graph_matches_enumerator();root=Path(__file__).resolve().parents[2];startsha=gitsha(root);t0=time.perf_counter()
    flip=hs1.hidden_flip_automorphism(hs1.HIDDEN_EDGES,hs1.HIDDEN_STATES)
    R=hs1.PartitionSearch("hidden_hs2",hs1.HIDDEN_STATES,hs1.HIDDEN_EDGES,output_record_limit=100000,automorphism=flip).run()
    assert not R.aborted and not R.error_count and R.feasible_count==EXPECTED_N and R.rank_distribution==EXPECTED_RANKS and R.feasible_stream_hash==EXPECTED_HASH and len(R.feasible_records)==EXPECTED_N
    tab=hs1.equality_row_table(hs1.HIDDEN_EDGES,hs1.HIDDEN_STATES);pb=pair_bases(a.max_n,lambda n:hstate(n,hs0,hs1)); reasons=Counter(); h=hashlib.sha256(); sh=hashlib.sha256(); survivors=[]
    for lab,er in R.feasible_records:
        ok,rank,p,b=hs1.exact_rref(hs1.rows_for_partition(lab,tab),21);assert ok and rank==er
        d,g,v=unpack(p,b,8); pos,pdet=positive(hs1.HIDDEN_EDGES,g,v); w=None if pos else pdet
        if w is None:w=direct(pb,d,g) if rank==21 else affine(pb,d,g,v)
        if w is None:
            rec={"labels":list(lab),"rank":rank,"status":"HS2_SIEVE_SURVIVOR_ONLY","positive_height":pdet,"max_n":a.max_n};survivors.append(rec);sh.update(record_bytes(rec));reason="survivor"
        else:rec={"labels":list(lab),"rank":rank,"reason":w["kind"],"witness":w};reason=w["kind"]
        reasons[reason]+=1;h.update(record_bytes(rec))
    assert sum(reasons.values())==EXPECTED_N
    out=a.output_dir or root/f"runs_hs2_{time.strftime('%Y%m%d_%H%M%S')}";out.mkdir(parents=True,exist_ok=True)
    summary={"status":"PASS","scope":"phi=0x0042 free-scale valuation-certified tagged-lift necessary-condition sieve","starting_git_sha":startsha,"python":platform.python_version(),"dependencies":"standard library only","normalization":{"scale_relation":"v2(|A|^2)=v2(M)","anchor_pair":[0,3]},"hs1_replay":{"feasible":R.feasible_count,"rank_distribution":{"21/0":59135,"18/3":119},"stream_sha256":R.feasible_stream_hash},"max_n":a.max_n,"max_n_semantics":"finite exact witness search only; survival is not all-pair feasibility","reason_counts":dict(sorted(reasons.items())),"survivor_count":len(survivors),"all_hs1_survivors_eliminated":not survivors,"classification_sha256":h.hexdigest(),"survivor_sha256":sh.hexdigest(),"wall_time_seconds":time.perf_counter()-t0,"unresolved_error_count":0}
    (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    with (out/"reason_counts.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(("reason","count"));w.writerows(sorted(reasons.items()))
    if survivors:
        with (out/"survivors.jsonl").open("w") as f:
            for x in survivors:f.write(json.dumps(x,sort_keys=True)+"\n")
    print("HS2 NORMALIZED VALUATION SIEVE PASS");print(json.dumps(summary,indent=2,sort_keys=True));print("output directory:",out);return 0

if __name__=="__main__":raise SystemExit(main())
