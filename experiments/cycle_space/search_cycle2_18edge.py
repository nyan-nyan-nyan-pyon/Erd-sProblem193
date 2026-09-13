#!/usr/bin/env python3
"""CYCLE2: exact-five equality census for the two 18-edge quarter-turn representatives.

Searches in cycle space using completed simple-cycle equations in five physical-step
variables. It does not perform any direct-geometry scan.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, platform, subprocess, sys, time
from collections import Counter
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from pathlib import Path

SEARCH_MASKS = (0x0002, 0x0004)
TARGET_BLOCKS = 5
EXPECTED_HS1_N = 59254
EXPECTED_HS1_RANKS = Counter({(21,0):59135,(18,3):119})
EXPECTED_HS1_HASH = "6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b"
EXPECTED_ORBITS = (
    (0x0002,0x0020,0x0046,0x0200),
    (0x0004,0x0040,0x0062,0x0242),
)
UNIT=((1,0),(0,1),(-1,0),(0,-1))

def load(path:Path,name:str):
    sp=importlib.util.spec_from_file_location(name,path)
    if sp is None or sp.loader is None: raise RuntimeError(path)
    m=importlib.util.module_from_spec(sp); sys.modules[name]=m; sp.loader.exec_module(m); return m

def modules(root:Path):
    cycle1=load(root/"experiments"/"cycle_space"/"analyze_cycle_space.py","cycle2_cycle1")
    hs0,hs1=cycle1.modules(root)
    return cycle1,hs0,hs1

def gitsha(root):
    return subprocess.run(["git","rev-parse","HEAD"],cwd=root,check=True,capture_output=True,text=True).stdout.strip()

def canonical_labels(labels):
    mp={}; out=[]; nxt=0
    for x in labels:
        if x not in mp: mp[x]=nxt; nxt+=1
        out.append(mp[x])
    return tuple(out)

@lru_cache(maxsize=None)
def rgs_count(remaining:int, used:int, target:int=5)->int:
    if used>target or used+remaining<target: return 0
    if remaining==0: return int(used==target)
    total=used*rgs_count(remaining-1,used,target)
    if used<target: total+=rgs_count(remaining-1,used+1,target)
    return total

def stirling(n,k):
    if n==0:return int(k==0)
    return rgs_count(n-1,1,k) if k else 0

def add_shared_row(basis, coeffs, rhs):
    """Add coeffs*x=rhs for two RHS columns (real,imag); exact reduced basis."""
    work=[F(x) for x in coeffs]+[F(rhs[0]),F(rhs[1])]
    for row in basis:
        p=next((i for i in range(5) if row[i]),None)
        if p is not None and work[p]:
            a=work[p]
            work=[x-a*y for x,y in zip(work,row)]
    if all(work[i]==0 for i in range(5)):
        return (work[5]==0 and work[6]==0), basis
    p=next(i for i in range(5) if work[i])
    a=work[p]; work=[x/a for x in work]
    out=[]
    for row in basis:
        if row[p]:
            a=row[p]
            out.append(tuple(x-a*y for x,y in zip(row,work)))
        else: out.append(row)
    out.append(tuple(work))
    out.sort(key=lambda row: next(i for i in range(5) if row[i]))
    return True,tuple(out)

def cycle_records(cycle1, states, edges):
    cycles=cycle1.simple_directed_cycles(states,edges)
    idx={e:i for i,e in enumerate(edges)}
    recs=[]
    for c in cycles:
        eis=tuple(idx[(c[i],c[(i+1)%len(c)])] for i in range(len(c)))
        re=im=0
        for s in c:
            x,y=UNIT[s[0]]; re+=x; im+=y
        recs.append({"states":c,"edges":eis,"edge_set":frozenset(eis),"rhs":(re,im)})
    q=len(edges)-len(states)+1
    incidence=[]
    for rec in recs:
        row=[0]*len(edges)
        for e in rec["edges"]: row[e]+=1
        incidence.append(tuple(row))
    assert cycle1.matrix_rank(incidence)==q
    return recs

def greedy_order(edge_count,recs):
    assigned=set(); out=[]
    while len(out)<edge_count:
        best=None
        for e in range(edge_count):
            if e in assigned: continue
            na=assigned|{e}
            completed=sum(1 for r in recs if e in r["edge_set"] and r["edge_set"]<=na and not r["edge_set"]<=assigned)
            one=sum(1 for r in recs if e in r["edge_set"] and len(r["edge_set"]-na)==1)
            two=sum(1 for r in recs if e in r["edge_set"] and len(r["edge_set"]-na)==2)
            part=sum(1 for r in recs if e in r["edge_set"])
            score=(completed,one,two,part,-e)
            if best is None or score>best[0]: best=(score,e)
        out.append(best[1]);assigned.add(best[1])
    return tuple(out)

def row_for_cycle(rec,labels, overrides=None):
    cnt=[0]*5
    for e in rec["edges"]:
        lab = overrides[e] if overrides and e in overrides else labels[e]
        if lab < 0: return None
        cnt[lab]+=1
    return tuple(cnt)

def lookahead_possible(basis, labels, recs, max_missing=2):
    """Safe over-approximation: future edges may use any of five colors."""
    for rec in recs:
        missing=[e for e in rec["edges"] if labels[e]<0]
        if not missing or len(missing)>max_missing: continue
        base=[0]*5
        for e in rec["edges"]:
            if labels[e]>=0: base[labels[e]]+=1
        ok_any=False
        for vals in product(range(5), repeat=len(missing)):
            cnt=base[:]
            for v in vals: cnt[v]+=1
            ok,_=add_shared_row(basis,cnt,rec["rhs"])
            if ok:
                ok_any=True;break
        if not ok_any:return False
    return True

def record_bytes(x):
    return (json.dumps(x,sort_keys=True,separators=(",",":"))+"\n").encode()

class Search:
    def __init__(self, cycle1, hs0, mask, edge_order=None, record_limit=200000, use_lookahead=True):
        self.cycle1=cycle1; self.hs0=hs0; self.mask=mask
        self.states=tuple(sorted(hs0.reachable(mask)))
        self.edges=tuple(edge_order) if edge_order is not None else tuple(sorted(hs0.adjacent_edges(mask)))
        assert set(self.edges)==set(hs0.adjacent_edges(mask))
        self.recs=cycle_records(cycle1,self.states,self.edges)
        self.order=greedy_order(len(self.edges),self.recs)
        self.by_edge=[[] for _ in self.edges]
        for ri,r in enumerate(self.recs):
            for e in r["edges"]:self.by_edge[e].append(ri)
        self.labels=[-1]*len(self.edges)
        self.record_limit=record_limit
        self.use_lookahead=use_lookahead
        self.nodes=0; self.prune_inconsistent=0; self.prune_lookahead=0
        self.logical_pruned=0; self.leaf_consistent=0
        self.rank_counts=Counter(); self.records=[]
        self.stream_hash=hashlib.sha256()
        self.max_basis_rank=0

    def completed_rows_after(self,e,basis):
        b=basis
        for ri in self.by_edge[e]:
            rec=self.recs[ri]
            if all(self.labels[x]>=0 for x in rec["edges"]):
                cnt=row_for_cycle(rec,self.labels)
                ok,b=add_shared_row(b,cnt,rec["rhs"])
                if not ok:return False,b
        return True,b

    def dfs(self,pos,used,basis):
        self.nodes+=1
        n=len(self.order)
        if pos==n:
            if used!=5:return
            self.leaf_consistent+=1
            rank=len(basis); self.rank_counts[rank]+=1
            labs=canonical_labels(self.labels)
            h=5-rank
            rec={"labels":list(labs),"cycle_rank":rank,"h":h}
            self.stream_hash.update(record_bytes(rec))
            if len(self.records)<self.record_limit:self.records.append((labs,rank))
            return

        e=self.order[pos]
        maxlab=min(used,4)
        for lab in range(maxlab+1):
            if lab==used:
                if used>=5:continue
                nu=used+1
            else:nu=used
            rem=n-pos-1
            if nu+rem<5:continue
            self.labels[e]=lab
            ok,nb=self.completed_rows_after(e,basis)
            if not ok:
                self.prune_inconsistent+=1
                self.logical_pruned+=rgs_count(rem,nu,5)
                self.labels[e]=-1
                continue
            self.max_basis_rank=max(self.max_basis_rank,len(nb))
            if self.use_lookahead and not lookahead_possible(nb,self.labels,self.recs,2):
                self.prune_lookahead+=1
                self.logical_pruned+=rgs_count(rem,nu,5)
                self.labels[e]=-1
                continue
            self.dfs(pos+1,nu,nb)
            self.labels[e]=-1

    def run(self):
        t=time.perf_counter()
        self.dfs(0,0,())
        total=stirling(len(self.edges),5)
        accounted=self.logical_pruned+self.leaf_consistent
        assert accounted==total,(accounted,total)
        assert not self.rank_counts.get(3,0),("rank15_counterexample",self.rank_counts[3])
        assert not any(r<3 for r in self.rank_counts)
        return {
            "mask":f"0x{self.mask:04x}",
            "edge_count":len(self.edges),
            "simple_cycle_count":len(self.recs),
            "assignment_order":list(self.order),
            "nodes":self.nodes,
            "inconsistent_prunes":self.prune_inconsistent,
            "lookahead_prunes":self.prune_lookahead,
            "logical_exact5_total":total,
            "logical_pruned":self.logical_pruned,
            "consistent_leaf_count":self.leaf_consistent,
            "cycle_rank_distribution":dict(sorted(self.rank_counts.items())),
            "h0_rank21":self.rank_counts[5],
            "h1_rank18":self.rank_counts[4],
            "h2_rank15":self.rank_counts[3],
            "feasible_total_after_rank15_exclusion":self.rank_counts[5]+self.rank_counts[4],
            "feasible_stream_sha256":self.stream_hash.hexdigest(),
            "record_limit":self.record_limit,
            "records_retained":len(self.records),
            "wall_time_seconds":time.perf_counter()-t,
        }

def hidden_edge_order(hs1):
    return tuple((hs1.HIDDEN_STATES[s],hs1.HIDDEN_STATES[t]) for s,t in hs1.HIDDEN_EDGES)

def regression_phi0042(root,cycle1,hs0,hs1):
    flip=hs1.hidden_flip_automorphism(hs1.HIDDEN_EDGES,hs1.HIDDEN_STATES)
    old=hs1.PartitionSearch("cycle2_regression",hs1.HIDDEN_STATES,hs1.HIDDEN_EDGES,
                            output_record_limit=100000,automorphism=flip).run()
    assert not old.aborted and not old.error_count
    assert old.feasible_count==EXPECTED_HS1_N
    assert old.rank_distribution==EXPECTED_HS1_RANKS
    assert old.feasible_stream_hash==EXPECTED_HS1_HASH
    oldset={tuple(lab):rank for lab,rank in old.feasible_records}
    assert len(oldset)==EXPECTED_HS1_N

    new=Search(cycle1,hs0,0x0042,edge_order=hidden_edge_order(hs1),record_limit=100000,use_lookahead=True)
    summ=new.run()
    newset={labs:(21 if rank==5 else 18 if rank==4 else -1) for labs,rank in new.records}
    assert len(new.records)==summ["feasible_total_after_rank15_exclusion"]==EXPECTED_HS1_N
    assert len(newset)==EXPECTED_HS1_N
    assert set(newset)==set(oldset)
    for labs in oldset:
        assert oldset[labs]==newset[labs]
    assert summ["h0_rank21"]==59135 and summ["h1_rank18"]==119 and summ["h2_rank15"]==0
    return summ

def gauge_for_shift(hs0,mask,k,target):
    raw=0
    for j in range(4):
        old=(j-k)&3
        for r in range(4):
            if hs0.bit(mask,old,r): raw|=1<<(4*j+r)
    hits=[g for g in hs0.GAUGES if hs0.gauge_transform(raw,g)==target]
    assert hits
    return hits[0]

def state_transport(s,k,g):
    j,h=s; jp=(j+k)&3
    return (jp,h^g[jp])

def verify_quarter_turn_transport(cycle1,hs0):
    orbits=cycle1.rotation_orbits(cycle1.enumerate_target_masks(hs0),hs0)
    assert tuple(sorted(orbits))==tuple(sorted(EXPECTED_ORBITS))
    maps={}
    for orb in EXPECTED_ORBITS:
        rep=orb[0]
        Erep=tuple(sorted(hs0.adjacent_edges(rep)))
        for target in orb:
            found=None
            for k in range(4):
                if cycle1.shift_j_mask(rep,k,hs0)!=target:continue
                g=gauge_for_shift(hs0,rep,k,target)
                image=[(state_transport(s,k,g),state_transport(t,k,g)) for s,t in Erep]
                Et=tuple(sorted(hs0.adjacent_edges(target)))
                assert set(image)==set(Et)
                idx={e:i for i,e in enumerate(Et)}
                perm=tuple(idx[e] for e in image)
                assert sorted(perm)==list(range(18))
                found={"k":k,"g":list(g),"edge_permutation":list(perm)}
                break
            assert found is not None,(rep,target)
            maps[f"0x{rep:04x}->0x{target:04x}"]=found
    return maps

def read_cycle1_summary(root):
    s=json.loads((root/"data"/"cycle_space"/"summary.json").read_text())
    assert s["status"]=="PASS"
    assert s["rank15_short_cycle_excluded"] is True
    assert s["allowed_eight_state_tag_ranks_after_short_cycle_exclusion"]==[21,18]
    return s

def self_test(root):
    cycle1,hs0,hs1=modules(root)
    read_cycle1_summary(root)
    verify_quarter_turn_transport(cycle1,hs0)
    b=()
    ok,b=add_shared_row(b,(1,0,0,0,0),(1,0)); assert ok
    ok,b2=add_shared_row(b,(1,0,0,0,0),(0,0)); assert not ok
    assert stirling(18,5)==28958095545
    reg=regression_phi0042(root,cycle1,hs0,hs1)
    print("CYCLE2 18-EDGE ENGINE SELF-TEST PASS")
    print(json.dumps(reg,indent=2,sort_keys=True))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--mask",type=lambda s:int(s,0),choices=SEARCH_MASKS)
    ap.add_argument("--all-representatives",action="store_true")
    ap.add_argument("--record-limit",type=int,default=200000)
    ap.add_argument("--no-lookahead",action="store_true")
    ap.add_argument("--output-dir",type=Path)
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[2]
    if args.self_test:
        self_test(root); return 0
    cycle1,hs0,hs1=modules(root)
    c1=read_cycle1_summary(root)
    transports=verify_quarter_turn_transport(cycle1,hs0)
    masks=SEARCH_MASKS if args.all_representatives else ((args.mask,) if args.mask is not None else ())
    if not masks: ap.error("choose --mask 0x0002/0x0004 or --all-representatives")
    start_sha=gitsha(root)
    out=args.output_dir or root/f"runs_cycle2_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True,exist_ok=True)
    results=[]
    for mask in masks:
        S=Search(cycle1,hs0,mask,record_limit=args.record_limit,use_lookahead=not args.no_lookahead)
        summ=S.run(); results.append(summ)
        (out/f"result_{mask:04x}.json").write_text(json.dumps(summ,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        if summ["feasible_total_after_rank15_exclusion"] <= args.record_limit:
            with (out/f"survivors_{mask:04x}.jsonl").open("w",encoding="utf-8") as f:
                for labs,rank in S.records:
                    f.write(json.dumps({"labels":list(labs),"cycle_rank":rank,"h":5-rank},sort_keys=True)+"\n")
    summary={
        "status":"PASS",
        "scope":"18-edge exact-five equality census in cycle space; no geometry",
        "starting_git_sha":start_sha,
        "python":platform.python_version(),
        "dependencies":"standard library only",
        "searched_representatives":[f"0x{x:04x}" for x in masks],
        "quarter_turn_orbits":[[f"0x{x:04x}" for x in o] for o in EXPECTED_ORBITS],
        "transport_maps":transports,
        "cycle1_starting_sha":c1["starting_git_sha"],
        "results":results,
        "unresolved_error_count":0,
    }
    (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print("CYCLE2 18-EDGE EQUALITY SEARCH PASS")
    print(json.dumps(summary,indent=2,sort_keys=True))
    print("output directory:",out)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
