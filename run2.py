import sys
from collections import deque, defaultdict


def solve(edges):
    graph = defaultdict(set)
    nodes = set()

    for u, v in edges:
        if not u or not v:
            continue

        graph[u].add(v)
        graph[v].add(u)
        nodes.add(u)
        nodes.add(v)

    def is_gateway(node):
        return node.isupper()

    gateways = {n for n in nodes if is_gateway(n)}

    virus = "a"
    if virus not in nodes:
        return []

    def bfs_with_parents(start):
        dist = {start: 0}
        parent = {}
        q = deque([start])
        while q:
            cur = q.popleft()

            for neighbour in sorted(graph[cur]):
                if neighbour not in dist:
                    dist[neighbour] = dist[cur] + 1
                    parent[neighbour] = cur
                    q.append(neighbour)
        return dist, parent

    def find_nearest_gate(start):
        dist, parent = bfs_with_parents(start)
        reachable = [(g, dist[g]) for g in gateways if g in dist]

        if not reachable:
            return None, None, None, None

        min_d = min(d for _, d in reachable)
        candidates = sorted([g for g, d in reachable if d == min_d])
        return candidates[0], min_d, dist, parent

    def rebuild_predposledniy_make_first_step(target, parent, start):

        path_rev = [target]
        cur = target

        while cur != start:
            if cur not in parent:
                return None, start
            cur = parent[cur]
            path_rev.append(cur)

        path = list(reversed(path_rev))

        if len(path) < 2:
            return None, start

        predposl = path[-2]
        first_step = path[1] if len(path) > 1 else start
        return predposl, first_step

    result = []

    while True:
        chosen_gw, dist_to_gw, dist_map, parent_map = find_nearest_gate(virus)
        if chosen_gw is None:
            break

        prepdosl, _ = rebuild_predposledniy_make_first_step(chosen_gw, parent_map, virus)

        off_edge_gw = chosen_gw
        off_edge_node = prepdosl

        if off_edge_node is None or off_edge_node not in graph.get(off_edge_gw, set()) or off_edge_gw not in graph.get(
                off_edge_node, set()):

            candidates = []

            for g in sorted(gateways):
                for n in sorted(graph.get(g, set())):
                    if not is_gateway(n):
                        candidates.append((g, n))

            if not candidates:
                break

            off_edge_gw, off_edge_node = candidates[0]

        if off_edge_node in graph.get(off_edge_gw, set()):
            graph[off_edge_gw].remove(off_edge_node)

        if off_edge_gw in graph.get(off_edge_node, set()):
            graph[off_edge_node].remove(off_edge_gw)

        result.append(f"{off_edge_gw}-{off_edge_node}")

        chosen_gw_after, _, _, parent_after = find_nearest_gate(virus)

        if not chosen_gw_after:
            break

        predposl_after, first_step_after = rebuild_predposledniy_make_first_step(chosen_gw_after, parent_after, virus)

        if first_step_after is None:
            break

        virus = first_step_after

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
