"""
A script that with functions to grey scale color graphs
"""

def grey_rainbow(n, black=False):
    """
Return n greyscale colors
"""
    if black:
        clrs = [0.299*clr[0] + 0.587 * clr[1] + 0.114 * clr[2] for clr in rainbow(n-2,'rgbtuple')]
    else:
        clrs = [0.299*clr[0] + 0.587 * clr[1] + 0.114 * clr[2] for clr in rainbow(n-1,'rgbtuple')]
    output = ['white']
    for c in clrs:
        if c <= 0.0031308:
            rgb = 12.92 * c
        else:
            rgb = (1.055*c^(1/2.4)-0.055)
        output.append((rgb,rgb,rgb))
    if black:
        output.append('black')
    return output

def grey_coloring(G, black=False):
    chromatic_nbr = G.chromatic_number()
    coloring = G.coloring()
    grey_colors = grey_rainbow(chromatic_nbr, black)
    d = {}
    for i, c in enumerate(grey_colors):
        d[c] = coloring[i]
    return P.graphplot(vertex_colors=d)


P = graphs.PetersenGraph()

p = grey_coloring(P)
p.show(figsize=[7,7])

p = grey_coloring(P, black=True)
p.show(figsize=[7,7])
