import sys
from collections import deque, defaultdict
from typing import List, Any


def solve(edges: tuple[str, str]) -> [str]:
    graph = defaultdict(set)
    nodes = set()

    for u, v in edges:

        if not u or not v:
            continue
        graph[u].add(v)
        graph[v].add(u)
        nodes.add(u)
        nodes.add(v)

    def is_gateway(node: str) -> bool:
        return node.isupper()

    gateways = {n for n in nodes if is_gateway(n)}

    virus = "a"
    if virus not in nodes:
        return []

    def bfs_with_parents(start: str) -> ({str, int}, {str, str}):
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

    def find_nearest_gate(start: str):
        dist, parent = bfs_with_parents(start)
        reachable = [(g, dist[g]) for g in gateways if g in dist]
        if not reachable:
            return None, None, None, None
        min_d = min(d for _, d in reachable)
        candidates = sorted([g for g, d in reachable if d == min_d])
        return candidates[0], min_d, dist, parent

    def reconstruct_path(parent: {str, str}, start: str, target: str) -> list[str | Any] | None:
        path = [target]
        cur = target
        while cur != start:
            if cur not in parent:
                return None
            cur = parent[cur]
            path.append(cur)
        path.reverse()
        return path

    result = []

    while True:
        chosen_gw, dist_to_gw, dist_map, parent_map = find_nearest_gate(virus)
        if chosen_gw is None:
            break

        path = reconstruct_path(parent_map, virus, chosen_gw)
        if not path or len(path) < 2:

            candidates = []
            for g in sorted(gateways):
                for n in sorted(graph.get(g, set())):
                    if not is_gateway(n):
                        candidates.append((g, n))
            if not candidates:
                break
            off_edge_gw, off_edge_node = candidates[0]

        else:

            pre_to_gateway = path[-2]
            off_edge_gw = chosen_gw
            off_edge_node = pre_to_gateway

            if off_edge_node not in graph.get(off_edge_gw, set()):
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

        path_after = reconstruct_path(parent_after, virus, chosen_gw_after)
        if not path_after or len(path_after) < 2:
            break

        first_step_after = path_after[1]
        virus = first_step_after

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        node1, sep, node2 = line.partition('-')
        if sep:
            edges.append((node1.strip(), node2.strip()))
    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
