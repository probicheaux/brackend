from math import log2

from numpy import math


def seed(seeds):
    num_seeds = len(seeds)
    seeds = [[i] for i in seeds]
    remain = 2 ** math.ceil(log2(num_seeds))
    remain = int(remain) - num_seeds
    seeds = seeds + [[num_seeds + 1]] * remain

    def pair_seeds(seeds):
        if len(seeds) == 1:
            return seeds
        out = list()
        while seeds:
            a = seeds.pop(0)
            b = seeds.pop()
            out.append(a + b)
        return pair_seeds(out)

    return pair_seeds(seeds)[0]


def match(l, all_matches, num_seeds):
    matches = []
    for i in range(len(l) // 2):
        proposed_match = tuple(l[i * 2 : i * 2 + 2])
        if not any([proposed_match in all_matches, reverse(proposed_match) in all_matches]):
            matches.append(proposed_match)
        else:
            if num_seeds + 1 not in proposed_match:
                raise ValueError
            else:
                matches.append(proposed_match)

    return matches


def reverse(tup):
    return (tup[1], tup[0])


def match_losers(from_losers, from_winners, round_index):
    matches = []
    assert len(from_losers) == len(from_winners)
    if len(from_losers) == 1:
        return [(from_losers[0], from_winners[0])]

    round_index = round_index % 4
    if round_index % 4 == 0:
        pass
    elif round_index % 4 == 1:
        midpoint = len(from_winners) // 2
        from_winners = from_winners[midpoint:] + from_winners[:midpoint]
    elif round_index % 4 == 2:
        midpoint = len(from_winners) // 2
        from_winners = from_winners[midpoint:] + from_winners[:midpoint]
        from_winners = from_winners[::-1]
    elif round_index % 4 == 3:
        from_winners = from_winners[::-1]
    else:
        assert False

    for p1, p2 in zip(from_losers, from_winners):
        proposed_match = (p1, p2)
        matches.append(proposed_match)

    return matches


def run_bracket(num_seeds):
    all_matches = []
    seeds = list(range(1, num_seeds + 1))
    winners = seed(seeds)
    matches = match(winners, all_matches, num_seeds)
    all_matches.extend(matches)
    winners = [min(m) for m in matches]
    losers = [max(m) for m in matches]
    round_index = 0
    while len(winners) > 1:
        print(f"Losers {2*round_index + 1}")
        losers_matches = match(losers, all_matches, num_seeds)
        print(losers_matches)
        all_matches.extend(losers_matches)
        winning_losers = [min(m) for m in losers_matches]

        matches = match(winners, all_matches, num_seeds)
        all_matches.extend(matches)
        winners = [min(m) for m in matches]
        losers = [max(m) for m in matches]

        losers_matches_2 = match_losers(winning_losers, losers[::-1], round_index)
        print(f"Losers {2*(round_index+1)}")
        print(losers_matches_2)
        losers = [min(m) for m in losers_matches_2]
        all_matches.extend(losers_matches_2)
        round_index += 1


if __name__ == "__main__":
    run_bracket(256)
