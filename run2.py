import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    nodes = set()
    res = []

    for u, v in edges:
        if not u or not v:
            continue
        graph[u].add(v)
        graph[v].add(u)
        nodes.add(u)
        nodes.add(v)

    def gateway(x: str) -> bool:
        return x.isupper()

    gateways = {n for n in nodes if gateway(n)}

    virus = "a"
    if virus not in nodes:
        return []

    def bfs(start: str, mode="all") -> dict[str, int]:
        queue = deque([start])
        dist = {start: 0}

        while queue:
            cur = queue.popleft()

            for nb in sorted(graph[cur]):
                if mode == "lower" and not nb.islower():
                    continue
                if nb not in dist:
                    dist[nb] = dist[cur] + 1
                    queue.append(nb)

        return dist

    def available_nodes(start: str) -> set[str]:
        if start not in graph:
            return set()

        comp = set(bfs(start, "lower").keys())
        return comp

    def front_edges(comp: set[str]) -> list[tuple[str, str]]:

        front = []
        for u in sorted(comp):
            for nb in sorted(graph[u]):
                if gateway(nb):
                    front.append((nb, u))
        front = sorted(front)
        return front

    while True:
        component = available_nodes(virus)
        front = front_edges(component)

        if not front:
            break

        virus_incident = [e for e in front if e[1] == virus]
        candidates = virus_incident if virus_incident else front

        cut_gw, cut_node = min(candidates)

        if cut_node in graph.get(cut_gw, set()):
            graph[cut_gw].remove(cut_node)

        if cut_gw in graph.get(cut_node, set()):
            graph[cut_node].remove(cut_gw)

        res.append(f"{cut_gw}-{cut_node}")

        comp_after = available_nodes(virus)
        front_after = front
        if not front_after:
            break

        dist_from_virus = bfs(virus)
        reachable_gates = [g for g in gateways if g in dist_from_virus]
        if not reachable_gates:
            break

        min_dist = min(dist_from_virus[g] for g in reachable_gates)
        candidate_gates = sorted([g for g in reachable_gates if dist_from_virus[g] == min_dist])
        target_gate = candidate_gates[0]

        go = bfs(target_gate)

        future_moves = []
        for nb in sorted(graph[virus]):
            if not nb.islower():
                continue

            dv = go.get(virus, None)
            dn = go.get(nb, None)
            if dv is None or dn is None:
                continue
            if dn == dv - 1:
                future_moves.append(nb)

        if future_moves:
            virus = min(future_moves)
        else:
            break

    return res


def main() -> None:

    edges: list[tuple[str, str]] = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        node1, sep, node2 = line.partition('-')
        if sep:
            edges.append((node1, node2))
    for cut in solve(edges):
        print(cut)


if __name__ == "__main__":
    main()
