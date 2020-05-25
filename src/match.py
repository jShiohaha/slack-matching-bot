import itertools
import random

# external package imports
from collections import OrderedDict

def build_empty_graph(items):
    graph = OrderedDict()
    for item in items:
        graph[item] = []
    return graph


def build_graph(items, graph=None):
    if graph is None:
        graph = build_empty_graph(items)
    # constant 2 dictates combination size
    for group in list(itertools.combinations(items, 2)):
        n1, n2 = group[0], group[1]
        graph[n1].append(n2)
        graph[n2].append(n1)
    return graph


def remove_bidir_graph_edge(n1, n2, graph):
    if n2 in graph[n1]:
        graph[n1].remove(n2)
    if n1 in graph[n2]:
        graph[n2].remove(n1)


def assign_unmatched_members_to_existing_groups(members, matches, graph):
    def assign_additional_member(member, match):
        m1, m2 = match[0], match[1]
        remove_bidir_graph_edge(m1, member, graph)
        remove_bidir_graph_edge(m2, member, graph)
        match.append(member)

    unmatched_members = list()
    for member in members:
        # itererate through matches and greedily add odd_member to first pairing where someone
        # hasn't matched with one of the two members of the existing pair
        found_member_match = False
        for match in matches:
            # max pair size is 3
            if len(match) == 3:
                continue
            m1, m2 = match[0], match[1]
            # if person hasn't met with one of the people in the match
            if member in graph[m1] or member in graph[m2]:
                assign_additional_member(member, match)
                found_member_match = True
                break
        if not found_member_match:
            unmatched_members.append(member)
    return unmatched_members


def update_graph(individuals, graph):
    ''' diff map itself and individuals and add them to the graph '''
    # assume that previous_matches is sorted by the number of values (potential new matches)
    new_members = set(individuals).difference(set(graph.keys()))
    # no new members; return
    if len(new_members) == 0:
        return
    # add new members to list of existing members match possibilities
    list_of_new_members = list(new_members)
    for key in graph.keys():
        graph[key].extend(list_of_new_members)
    all_members = set(individuals + list(graph.keys()))
    for m in new_members:
        # add all members (except self) to list of new members match possibilities
        graph[m] = list(all_members.difference({m}))
    return


def generate_matches(individuals, graph):
    # no individuals to match
    if len(individuals) == 0:
        return -1, list()
    if graph is None:
        graph = build_graph(individuals)
    else:
        update_graph(individuals, graph)
    # sort function nlogn is worse as n -> infinity
    graph = OrderedDict(sorted(graph.items(), key=lambda x: len(x[1])))

    matches = list() # a match item is of the form [m1, m2]
    unmatched_members = set() # a match item is of the form [m1, ]
    members_with_no_matches = set() # a match item is of the form [m1, ]
    set_of_members = set(individuals)

    # after updating the graph; only iterate through and remove people that don't have any match potentials
    for k, v in graph.items():
        if len(v) > 0:
            break # since the graph is sorted, exit as soon as len of potential matches >1
        members_with_no_matches.add(k)
        set_of_members.remove(k)

    odd_member = None
    if len(set_of_members) > 0 and len(set_of_members) % 2 == 1:
        # always choose someone with the fewest possible partners left
        min_possible_partners = min([len(v) for v in graph.values() if len(v) != 0])
        odd_member = random.choice([member for member in set_of_members if len(graph[member]) <= min_possible_partners])
        # remove odd member from set_of_members
        set_of_members.remove(odd_member)
        unmatched_members.add(odd_member)

    # better to just iterate through people in the channel; in the correct order
    for k, v in graph.items():
        if k not in set_of_members:
            continue
        possible_partners = list(set_of_members & set(graph[k]))
        # no possible partners for this member
        if len(possible_partners) == 0:
            unmatched_members.add(k)
        else:
            partner = random.choice(possible_partners)
            remove_bidir_graph_edge(k, partner, graph)
            matches.append([k, partner])
            # remove members from this match from future consideration
            set_of_members.remove(k)
            set_of_members.remove(partner)
    unmatched_members = assign_unmatched_members_to_existing_groups(unmatched_members, matches, graph)
    
    num_matches = len(matches)
    num_unmatched = len(unmatched_members)
    matches.extend(list(unmatched_members))
    matches.extend(list(members_with_no_matches))
    # n matches, m unmatched, len(matches)-n-m impossible matches
    return num_matches, matches # TODO: (num_matches, num_unmatched, len(matches)-num_matches-num_unmatched)
