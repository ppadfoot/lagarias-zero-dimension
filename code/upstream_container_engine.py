#!/usr/bin/env python3
"""Exact finite audit of the strengthened full-origin budget C*Q**(r-3).

This is an executable check of a separate universal proof.  It does not
establish the S-unit theorem or a dimension result by finite enumeration.
Python 3.10+, standard library, assertions enabled.
"""
from collections import Counter, defaultdict, deque
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

assert __debug__, 'Run without -O.'


def merge_counts(target, source):
    target.update({k:v for k,v in source.items() if k != 'max_positive_query_depth'})
    target['max_positive_query_depth'] = max(target.get('max_positive_query_depth', 0),
                                              source.get('max_positive_query_depth', 0))


class Model:
    def __init__(self, name, length, q, templates, kind, seed=0, query_order='min'):
        self.name, self.length, self.q = name, length, q
        self.N, self.Q = length-q+1, 2**q
        self.templates, self.kind, self.seed = templates, kind, seed
        self.query_order = query_order
        assert query_order in ('min', 'max')
        self.r = len(templates[0])
        assert self.r >= 3 and all(len(t) == self.r for t in templates)
        self.edges = defaultdict(list)
        pair_degrees = Counter()
        for i in range(self.N):
            destinations = []
            for s, offsets in enumerate(templates):
                assert offsets[0] == 0 and list(offsets) == sorted(set(offsets))
                assert all(b-a >= q for a, b in zip(offsets, offsets[1:]))
                positions = tuple(i+x for x in offsets)
                if positions[-1] < self.N:
                    self.edges[i].append((s, positions[1:]))
                    destinations.extend(positions[1:])
                    pair_degrees.update(combinations(positions, 2))
            assert len(destinations) == len(set(destinations)), 'Future positions must form a matching at each source.'
        self.C = max(pair_degrees.values(), default=1)
        assert self.C <= self.r*(self.r-1)//2
        self.D = self.C*self.Q**(self.r-3)

    @lru_cache(None)
    def allowed(self, i, s, prefix, letters):
        if prefix == 0 and all(a == 0 for a in letters):
            return True
        phase = (prefix.bit_count()+3*i+5*s+self.seed) % 17
        if self.kind == 'sparse':
            value = sum((2*k+3)*a for k, a in enumerate(letters))+phase
            return value % 11 not in (1, 3)
        if self.kind == 'xor':
            target = phase % self.Q
            for a in letters[:-1]:
                target ^= a
            return letters[-1] != target
        raise AssertionError(self.kind)

    def feasible(self, word):
        for i, edges in self.edges.items():
            prefix = word % 2**i
            a = (word >> i) % self.Q
            for s, targets in edges:
                letters = (a,)+tuple((word >> j) % self.Q for j in targets)
                if not self.allowed(i, s, prefix, letters):
                    return False
        return True


class Run:
    def __init__(self, model, word, T0, thresholds, supplied=None):
        self.m, self.word = model, word
        self.N, self.Q, self.r, self.D = model.N, model.Q, model.r, model.D
        self.T0, self.T, self.supplied = T0, dict(thresholds), supplied
        assert set(self.T) == set(range(2, self.r))
        self.actual = [(word >> i) % self.Q for i in range(self.N)]
        self.pal = [set(range(self.Q)) for _ in range(self.N)]
        self.active = {(i, a) for i in range(self.N) for a in range(self.Q)}
        self.adj = {j: defaultdict(set) for j in self.T}
        self.edges = {j: {} for j in self.T}
        self.ever = {j: set() for j in self.T}
        self.queues = {j: deque() for j in self.T}
        self.known, self.F, self.A = {}, {}, {}
        self.processed = set()
        self.origins, self.location = {}, {}
        self.origin_pairs = defaultdict(set)
        self.deletion_time = {}
        self.clock = 0
        self.stats = Counter()
        self.states, self.query_stack = [], []
        self.edge_charges = defaultdict(Counter)
        self.deletion_charges = defaultdict(Counter)
        self.witness_origins = defaultdict(set)

    def erase_edge(self, key):
        j = len(key)
        origins = self.edges[j].pop(key)
        for v in key:
            self.adj[j][v].remove(key)
        self.stats[f'removals_{j}'] += 1
        return origins

    def remove_active_vertex(self, v, reason):
        if v not in self.active:
            return
        for j in self.T:
            assert len(self.adj[j][v]) <= self.T[j]
            for key in sorted(self.adj[j][v]):
                origins = self.erase_edge(key)
                for o in origins:
                    self.location[o] = (reason, key if reason == 'retired' else v)
                if reason == 'retired':
                    self.stats[f'retired_edges_{j}'] += 1
        self.active.remove(v)
        self.stats['active_vertex_removals'] += 1

    def erase_letter(self, v):
        j, a = v
        if a not in self.pal[j]:
            return
        assert j not in self.processed and j not in self.known
        assert a != self.actual[j], 'An actual letter cannot be removed.'
        self.clock += 1
        self.deletion_time[v] = self.clock
        self.pal[j].remove(a)
        assert self.pal[j]
        self.remove_active_vertex(v, 'deleted')
        self.stats['palette_deletions'] += 1

    def enqueue(self, key, origins):
        key = tuple(sorted(key))
        assert len(key) >= 2
        for o in origins:
            self.location[o] = ('queued', key)
        self.queues[len(key)].append((key, set(origins)))
        if self.query_stack and len(key) >= self.query_stack[-1]:
            self.stats['higher_or_equal_rank_projections_deferred'] += 1

    def mark_known(self, j, a):
        assert j not in self.known and j not in self.processed
        assert a == self.actual[j] and a in self.pal[j]
        v = (j, a)
        pairs, projections = [], []
        for rank in self.T:
            for key in sorted(self.adj[rank][v]):
                origins = self.erase_edge(key)
                rest = tuple(x for x in key if x != v)
                if rank == 2:
                    pairs.append((rest[0], origins))
                else:
                    projections.append((rest, origins))
        self.F[j] = a
        self.known[j] = a
        # Graph neighbours are pruned before ANY pending projection is installed.
        for other, origins in pairs:
            self.erase_letter(other)
            for o in origins:
                self.location[o] = ('deleted', other)
        for b in sorted(self.pal[j]-{a}):
            # This exclusion is a consequence of revealing the actual letter.
            self.clock += 1
            self.deletion_time[j, b] = self.clock
            self.pal[j].remove(b)
            self.remove_active_vertex((j, b), 'deleted')
            self.stats['palette_deletions'] += 1
        self.remove_active_vertex(v, 'known')
        assert self.pal[j] == {a}
        for key, origins in projections:
            self.enqueue(key, origins)

    def query_actual(self, v):
        j, a = v
        return self.actual[j] == a if self.supplied is None else self.supplied.get(j) == a

    def choose_witness_origins(self, rank, keys):
        selected = []
        for key in keys:
            o = min(self.edges[rank][key])
            assert o not in self.witness_origins[rank]
            self.witness_origins[rank].add(o)
            selected.append(o)
        return selected

    def charge_batch(self, rank, witnesses, start_clock):
        for o in witnesses:
            kind, target = self.location[o]
            if kind == 'deleted':
                assert self.deletion_time[target] > start_clock
                self.deletion_charges[rank][target] += 1
                bound = 1 if rank == self.r else self.D
                assert self.deletion_charges[rank][target] <= bound
            else:
                assert kind == 'active', (rank, kind, target)
                assert len(target) < rank
                self.edge_charges[rank][target] += 1
                assert self.edge_charges[rank][target] <= self.D

    def install(self, key, origins):
        removed = next((v for v in key if v[1] not in self.pal[v[0]]), None)
        if removed is not None:
            for o in origins:
                self.location[o] = ('deleted', removed)
            return
        unknown = tuple(v for v in key if v[0] not in self.known)
        assert unknown, 'A fully known forbidden tuple would contradict feasibility.'
        if len(unknown) < len(key):
            self.stats['known_endpoint_reductions'] += 1
        if len(unknown) == 1:
            self.erase_letter(unknown[0])
            for o in origins:
                self.location[o] = ('deleted', unknown[0])
            self.stats['known_endpoint_prunings'] += 1
            return
        key, rank = unknown, len(unknown)
        assert all(v in self.active for v in key)
        if key in self.edges[rank]:
            self.edges[rank][key].update(origins)
            for o in origins:
                self.location[o] = ('active', key)
            self.stats['duplicate_promotions_merged'] += 1
            return
        assert key not in self.ever[rank], 'Removed active vertices can never return.'
        assert all(len(self.adj[rank][v]) < self.T[rank] for v in key)
        self.edges[rank][key] = set(origins)
        self.ever[rank].add(key)
        for v in key:
            self.adj[rank][v].add(key)
        for o in origins:
            self.location[o] = ('active', key)
        self.stats[f'insertions_{rank}'] += 1
        critical = [v for v in key if len(self.adj[rank][v]) >= self.T[rank]]
        if not critical:
            return
        v = min(critical) if self.m.query_order == 'min' else max(critical)
        assert len(self.adj[rank][v]) == self.T[rank]
        self.stats[f'queries_{rank}'] += 1
        if not self.query_actual(v):
            self.stats[f'negative_queries_{rank}'] += 1
            self.erase_letter(v)
            assert all(len(self.adj[rank][w]) < self.T[rank] for w in self.active)
            return
        self.stats[f'positive_queries_{rank}'] += 1
        start_clock = self.clock
        witnesses = self.choose_witness_origins(rank, sorted(self.adj[rank][v]))
        if self.query_stack:
            assert rank < self.query_stack[-1]
            self.stats['nested_strictly_lower_rank_positive_queries'] += 1
        self.query_stack.append(rank)
        self.stats['max_positive_query_depth'] = max(self.stats['max_positive_query_depth'], len(self.query_stack))
        self.mark_known(*v)
        # Higher-rank projections remain queued.  Only smaller ranks may
        # be installed while this positive-query packet is open.
        self.drain(rank)
        self.charge_batch(rank, witnesses, start_clock)
        assert self.query_stack.pop() == rank
        assert all(len(self.adj[rank][w]) < self.T[rank] for w in self.active)

    def drain(self, ceiling):
        while True:
            rank = next((j for j in range(2, ceiling) if self.queues[j]), None)
            if rank is None:
                return
            key, origins = self.queues[rank].popleft()
            self.install(key, origins)

    def register_origin(self, source, template, a, key):
        origin = (source, template, a, key)
        assert origin not in self.origins
        self.origins[origin] = key
        for pair in combinations(key, 2):
            self.origin_pairs[pair].add(origin)
            assert len(self.origin_pairs[pair]) <= self.D
        self.enqueue(key, {origin})
        return origin

    def links_for(self, i, a):
        links, witnesses = [], []
        prefix = self.word % 2**i
        for s, targets in self.m.edges[i]:
            local = []
            for values in product(*(sorted(self.pal[j]) for j in targets)):
                if not self.m.allowed(i, s, prefix, (a,)+values):
                    key = tuple(zip(targets, values))
                    local.append((s, key))
            if local:
                witnesses.append(local[0])
            links.extend(local)
        return links, witnesses

    def state_digest(self):
        assert all(not q for q in self.queues.values())
        state = (tuple(tuple(sorted(x)) for x in self.pal), tuple(sorted(self.known.items())),
                 tuple((j, tuple(sorted(self.edges[j]))) for j in self.T))
        return hashlib.sha256(repr(state).encode()).hexdigest()

    def run(self):
        for i in range(self.N):
            assert self.actual[i] in self.pal[i]
            assert all(len(self.adj[j][v]) < self.T[j] for j in self.T for v in self.active)
            self.states.append(self.state_digest())
            if i in self.known:
                chosen = self.known[i]
                links, _ = self.links_for(i, chosen)
                self.A[i] = {chosen}
                for s, key in links:
                    self.register_origin(i, s, chosen, key)
                    self.drain(self.r)
            else:
                data = {a: self.links_for(i, a) for a in sorted(self.pal[i])}
                heavy = {a for a, (_, witnesses) in data.items() if len(witnesses) >= self.T0}
                first_heavy = self.actual[i] in heavy if self.supplied is None else i in self.supplied
                chosen = self.actual[i] if self.supplied is None else self.supplied.get(i)
                if first_heavy:
                    assert chosen in heavy
                    self.stats['first_heavy_sources'] += 1
                    links, witnesses = data[chosen]
                    witness_keys = {(s, key) for s, key in witnesses}
                    positions = [j for _, key in witnesses for j, _ in key]
                    assert len(positions) == len(set(positions))
                    start_clock = self.clock
                    self.mark_known(i, chosen)
                    self.drain(self.r)
                    self.A[i] = {chosen}
                    witness_origins = []
                    for s, key in links:
                        o = self.register_origin(i, s, chosen, key)
                        if (s, key) in witness_keys:
                            witness_origins.append(o)
                        self.drain(self.r)
                    self.charge_batch(self.r, witness_origins, start_clock)
                    self.stats['first_heavy_witnesses'] += len(witness_origins)
                else:
                    self.A[i] = self.pal[i]-heavy
                    assert self.actual[i] in self.A[i]
            assert not self.query_stack and all(not q for q in self.queues.values())
            for a in sorted(self.pal[i]):
                self.remove_active_vertex((i, a), 'retired')
            self.processed.add(i)
        assert not self.active and all(not x for x in self.edges.values())
        total_insert = 0
        for j in self.T:
            insert = self.stats[f'insertions_{j}']
            assert insert == self.stats[f'removals_{j}'] <= self.T[j]*self.Q*self.N
            if j == 2:
                assert self.stats['positive_queries_2']*self.T[2] <= self.stats['palette_deletions']
            else:
                lower = sum(self.stats[f'insertions_{l}'] for l in range(2, j))
                assert self.stats[f'positive_queries_{j}']*self.T[j] <= self.D*(lower+self.stats['palette_deletions'])
            total_insert += insert
        assert len(self.F) == self.stats['first_heavy_sources']+sum(self.stats[f'positive_queries_{j}'] for j in self.T)
        assert self.stats['first_heavy_sources']*self.T0 <= self.D*total_insert+self.stats['palette_deletions']
        assert self.stats['palette_deletions'] <= (self.Q-1)*self.N
        bad, recorded_bad, terminal_charge = [], [], Counter()
        for i, edges in self.m.edges.items():
            prefix = self.word % 2**i
            for s, targets in edges:
                positions = (i,)+targets
                values = next((v for v in product(*(sorted(self.A[j]) for j in positions))
                               if not self.m.allowed(i, s, prefix, v)), None)
                if values is None:
                    continue
                bad.append((i, s, targets))
                if i in self.F:
                    assert values[0] == self.F[i]
                    origin = (i, s, values[0], tuple(zip(targets, values[1:])))
                    assert origin in self.origins
                    kind, terminal = self.location[origin]
                    assert kind == 'retired'
                    terminal_charge[terminal] += 1
                    assert terminal_charge[terminal] <= self.D
                    recorded_bad.append((i, s, targets))
        assert len(recorded_bad) <= self.D*total_insert
        assert len(bad)-len(recorded_bad) <= self.Q*self.T0*self.N
        assert len(bad) <= self.Q*(self.T0+self.D*sum(self.T.values()))*self.N
        self.stats['bad_hyperedges'] += len(bad)
        self.stats['recorded_source_bad_hyperedges'] += len(recorded_bad)
        self.stats['full_forbidden_origins'] += len(self.origins)
        self.stats['original_hyperedges'] += sum(map(len, self.m.edges.values()))
        return self


def check_model(model, thresholds, max_words=64, candidate_bits=None):
    candidate_bits = model.length if candidate_bits is None else candidate_bits
    assert 1 <= candidate_bits <= model.length
    feasible = [w for w in range(2**candidate_bits) if model.feasible(w)]
    assert feasible
    if len(feasible) > max_words:
        words = [feasible[k*(len(feasible)-1)//(max_words-1)] for k in range(max_words)]
    else:
        words = feasible
    totals = Counter()
    for T0, T in thresholds:
        runs = [Run(model, w, T0, T).run() for w in words]
        shared_states, supports = {}, defaultdict(set)
        for run in runs:
            fingerprint = tuple(sorted(run.F.items()))
            replay = Run(model, run.word, T0, T, dict(fingerprint)).run()
            assert replay.F == run.F and replay.A == run.A and replay.states == run.states
            assert replay.stats == run.stats
            totals['full_fingerprint_replays'] += 1
            for i in range(model.N):
                key = (fingerprint, i, run.word % 2**i)
                state = (run.states[i], tuple(sorted(run.A[i])))
                if key in shared_states:
                    assert shared_states[key] == state
                    totals['same_prefix_fingerprint_state_comparisons'] += 1
                else:
                    shared_states[key] = state
                supports[key].add((run.word >> i) % model.Q)
            merge_counts(totals, run.stats)
        for run in runs:
            fingerprint = tuple(sorted(run.F.items()))
            for i in range(model.N):
                key = (fingerprint, i, run.word % 2**i)
                assert supports[key] <= run.A[i]
                totals['actual_conditional_support_inclusions'] += 1
        totals['runs'] += len(runs)
    return {'name': model.name, 'arity': model.r, 'length': model.length,
            'q': model.q, 'alphabet_size': model.Q, 'pair_codegree': model.C,
            'origin_pair_codegree_bound': model.D,
            'candidate_word_count': 2**candidate_bits,
            'candidate_family': 'All binary words with positions at or above candidate_bits fixed to zero.',
            'candidate_bits': candidate_bits,
            'query_order': model.query_order,
            'feasible_in_candidate_family': len(feasible), 'tested_words': len(words),
            'thresholds': [(a, dict(b)) for a, b in thresholds], 'counts': dict(totals)}


def main():
    specifications = [
        (Model('triple_two_templates', 11, 1, [(0,1,2), (0,3,6)], 'sparse', 1),
         [(1, {2:2}), (2, {2:3})]),
        (Model('four_two_templates', 15, 1, [(0,1,2,3), (0,4,8,12)], 'sparse', 2),
         [(1, {2:2,3:3}), (2, {2:3,3:5}), (1, {2:8,3:2})]),
        (Model('four_overlapping_windows', 13, 2, [(0,2,4,6)], 'sparse', 3),
         [(1, {2:2,3:3}), (1, {2:7,3:2}), (2, {2:4,3:6})]),
        (Model('five_levels_nested', 13, 1, [(0,1,2,3,4)], 'sparse', 4),
         [(1, {2:2,3:3,4:4}), (1, {2:6,3:2,4:3}), (2, {2:3,3:4,4:6})]),
        (Model('five_overlapping_windows', 13, 2, [(0,2,4,6,8)], 'sparse', 7),
         [(1, {2:2,3:3,4:4}), (1, {2:8,3:2,4:5}), (2, {2:4,3:5,4:7})]),
        (Model('six_levels_nested', 12, 1, [(0,1,2,3,4,5)], 'sparse', 5),
         [(1, {2:2,3:3,4:4,5:5}), (1, {2:8,3:3,4:2,5:6}),
          (2, {2:3,3:4,4:5,5:7})]),
    ]
    results = [check_model(model, thresholds) for model, thresholds in specifications]
    results.append(check_model(
        Model('five_deferred_projection_packets', 23, 1,
              [(0,1,2,3,4), (0,5,10,15,20)], 'sparse', 4),
        [(1, {2:1,3:2,4:100}), (1, {2:2,3:4,4:100}),
         (1, {2:1,3:1,4:100}), (1, {2:2,3:2,4:10})],
        candidate_bits=16))
    results.append(check_model(
        Model('five_reverse_query_order', 16, 1,
              [(0,1,2,3,4)], 'sparse', 6, query_order='max'),
        [(1, {2:2,3:3,4:4}), (1, {2:8,3:3,4:6}),
         (1, {2:100,3:100,4:3}), (2, {2:3,3:4,4:6})],
        candidate_bits=14))
    totals = Counter()
    for result in results:
        merge_counts(totals, result['counts'])
    assert totals['higher_or_equal_rank_projections_deferred'] > 0
    assert totals['nested_strictly_lower_rank_positive_queries'] > 0
    assert totals['duplicate_promotions_merged'] > 0
    assert totals['known_endpoint_prunings'] > 0
    assert totals['recorded_source_bad_hyperedges'] > 0
    for j in range(2, 6):
        assert totals[f'positive_queries_{j}'] > 0
        assert totals[f'negative_queries_{j}'] > 0
    report = {'status': 'PASS', 'arithmetic': 'exact integers and finite sets',
              'scope': 'Targeted check of the sharper full-origin constant D=C*Q**(r-3) on the unchanged stage11 fixtures. All per-origin charges, queue invariants, full-fingerprint replay and support checks remain enabled. Universal proofs are separate.',
              'models': results, 'totals': dict(totals)}
    target = Path(__file__).with_name('sharp_origin_container_checks.json')
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status':'PASS', 'models':len(results), 'totals':dict(totals)}, indent=2))


if __name__ == '__main__':
    main()
