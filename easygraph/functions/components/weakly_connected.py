"""Weakly connected components."""
import easygraph as eg

from easygraph.utils.decorators import not_implemented_for


__all__ = [
    "number_weakly_connected_components",
    "weakly_connected_components",
    "is_weakly_connected",
]


@not_implemented_for("undirected")
def weakly_connected_components(G):
    """Generate weakly connected components of G.

    Parameters
    ----------
    G : EasyGraph graph
        A directed graph

    Returns
    -------
    comp : generator of sets
        A generator of sets of nodes, one for each weakly connected
        component of G.

    Raises
    ------
    EasyGraphNotImplemented
        If G is undirected.

    Examples
    --------
    Generate a sorted list of weakly connected components, largest first.

    >>> G = eg.path_graph(4, create_using=eg.DiGraph())
    >>> eg.add_path(G, [10, 11, 12])
    >>> [
    ...     len(c)
    ...     for c in sorted(eg.weakly_connected_components(G), key=len, reverse=True)
    ... ]
    [4, 3]

    If you only want the largest component, it's more efficient to
    use max instead of sort:

    >>> largest_cc = max(eg.weakly_connected_components(G), key=len)

    See Also
    --------
    connected_components
    strongly_connected_components

    Notes
    -----
    For directed graphs only.

    """
    seen = set()
    for v in G:
        if v not in seen:
            c = set(_plain_bfs(G, v))
            seen.update(c)
            yield c


@not_implemented_for("undirected")
def number_weakly_connected_components(G):
    """Returns the number of weakly connected components in G.

    Parameters
    ----------
    G : EasyGraph graph
        A directed graph.

    Returns
    -------
    n : integer
        Number of weakly connected components

    Raises
    ------
    EasyGraphNotImplemented
        If G is undirected.

    Examples
    --------
    >>> G = eg.DiGraph([(0, 1), (2, 1), (3, 4)])
    >>> eg.number_weakly_connected_components(G)
    2

    See Also
    --------
    weakly_connected_components
    number_connected_components
    number_strongly_connected_components

    Notes
    -----
    For directed graphs only.

    """
    return sum(1 for wcc in weakly_connected_components(G))


@not_implemented_for("undirected")
def is_weakly_connected(G):
    """Test directed graph for weak connectivity.

    A directed graph is weakly connected if and only if the graph
    is connected when the direction of the edge between nodes is ignored.

    Note that if a graph is strongly connected (i.e. the graph is connected
    even when we account for directionality), it is by definition weakly
    connected as well.

    Parameters
    ----------
    G : EasyGraph Graph
        A directed graph.

    Returns
    -------
    connected : bool
        True if the graph is weakly connected, False otherwise.

    Raises
    ------
    EasyGraphNotImplemented
        If G is undirected.

    Examples
    --------
    >>> G = eg.DiGraph([(0, 1), (2, 1)])
    >>> G.add_node(3)
    >>> eg.is_weakly_connected(G)  # node 3 is not connected to the graph
    False
    >>> G.add_edge(2, 3)
    >>> eg.is_weakly_connected(G)
    True

    See Also
    --------
    is_strongly_connected
    is_semiconnected
    is_connected
    is_biconnected
    weakly_connected_components

    Notes
    -----
    For directed graphs only.

    """
    if len(G) == 0:
        raise eg.EasyGraphPointlessConcept(
            """Connectivity is undefined for the null graph."""
        )

    return len(next(weakly_connected_components(G))) == len(G)


def _plain_bfs(G, source):
    """A fast BFS node generator

    The direction of the edge between nodes is ignored.

    For directed graphs only.

    """
    Gsucc = G.adj
    Gpred = G.pred

    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                nextlevel.update(Gsucc[v])
                nextlevel.update(Gpred[v])
                yield v
