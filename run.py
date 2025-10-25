import sys
import heapq

weights = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
enters = (2, 4, 6, 8)
stops = (0, 1, 3, 5, 7, 9, 10)


def solve(lines: list[str]) -> int:

    corridor_line = lines[1]
    corridor = tuple(corridor_line[1:12])
    depth = len(lines) - 3

    columns = (3, 5, 7, 9)
    rooms = tuple(tuple(lines[2 + lvl][columns[r]] for lvl in range(depth)) for r in range(4))

    target_rooms = tuple(tuple(chr(ord('A') + r) for _ in range(depth)) for r in range(4))

    def clear_path(cor: tuple[str, ...], start: int, end: int) -> bool:

        if start < end:
            rng = range(start + 1, end + 1)
        else:
            rng = range(end, start)
        for j in rng:
            if cor[j] != '.':
                return False
        return True

    def can_enter(room: tuple[str, ...], ch: str) -> bool:
        return all(c == '.' or c == ch for c in room)

    def rooms_depth(room: tuple[str, ...]) -> int | None:
        for i in range(depth - 1, -1, -1):
            if room[i] == '.':
                return i
        return None

    def room_top_index(room: tuple[str, ...]) -> int | None:
        for i in range(depth):
            if room[i] != '.':
                return i
        return None

    def neighbors(cor: tuple[str, ...], rms: tuple[tuple[str, ...], ...]):

        for h_idx, ch in enumerate(cor):
            if ch == '.':
                continue

            targ = ord(ch) - ord('A')
            room = rms[targ]
            if not can_enter(room, ch):
                continue
            enter = enters[targ]
            if not clear_path(cor, h_idx, enter):
                continue
            dest = rooms_depth(room)
            if dest is None:
                continue

            steps = abs(h_idx - enter) + (dest + 1)
            cost = steps * weights[ch]
            new_corridor = list(cor)
            new_corridor[h_idx] = '.'
            new_rooms = [list(r) for r in rms]
            new_rooms[targ][dest] = ch
            yield tuple(new_corridor), tuple(tuple(r) for r in new_rooms), cost

        for i in range(4):
            room = rms[i]
            top = room_top_index(room)

            if top is None:
                continue
            ch = room[top]

            if (ord(ch) - ord('A')) == i and all(c == ch for c in room[top:]):
                continue
            enter = enters[i]

            for stop in stops:

                if cor[stop] != '.':
                    continue
                if not clear_path(cor, enter, stop):
                    continue

                steps = (top + 1) + abs(enter - stop)
                cost = steps * weights[ch]
                new_corridor = list(cor)
                new_corridor[stop] = ch
                new_rooms = [list(rr) for rr in rms]
                new_rooms[i][top] = '.'
                yield tuple(new_corridor), tuple(tuple(rr) for rr in new_rooms), cost

    start = (corridor, rooms)
    pq = []
    heapq.heappush(pq, (0, start[0], start[1]))
    dist = {start: 0}

    while pq:
        cost, cur_cor, cur_rooms = heapq.heappop(pq)
        position = (cur_cor, cur_rooms)
        if dist.get(position, 10 ** 30) != cost:
            continue
        if cur_rooms == target_rooms and all(x == '.' for x in cur_cor):
            return cost

        for nh, nr, add in neighbors(cur_cor, cur_rooms):
            n_pos = (nh, nr)
            nc = cost + add
            if nc < dist.get(n_pos, 10 ** 30):
                dist[n_pos] = nc
                heapq.heappush(pq, (nc, nh, nr))

    return -1


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    if not lines:
        return
    print(solve(lines))

if __name__ == "__main__":
    main()
