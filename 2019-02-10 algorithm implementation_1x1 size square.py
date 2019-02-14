def gridify(moves):
    grid = (0, 0)
    grids = {grid}
    edges = set()
    for i in moves:
        if i == 'U': 
            edge = (grid[0], grid[1], grid[0], grid[1] + 1)
            grid = edge[-2:]
        elif i == 'D': 
            edge = (grid[0], grid[1] - 1, grid[0], grid[1])
            grid = edge[:2]
        elif i == 'R': 
            edge = (grid[0], grid[1], grid[0] + 1, grid[1])
            grid = edge[-2:]
        else: 
            edge = (grid[0] - 1, grid[1], grid[0], grid[1])
            grid = edge[:2]
        grids.add(grid)
        edges.add(edge)
    return sorted(list(grids)), edges

def square(pt):
    ed1 = (pt[0], pt[1], pt[0], pt[1] + 1)
    ed2 = (pt[0], pt[1] + 1, pt[0] + 1, pt[1] + 1)
    ed3 = (pt[0], pt[1], pt[0] + 1, pt[1])
    ed4 = (pt[0] + 1, pt[1], pt[0] + 1, pt[1] + 1)
    return [ed1, ed2, ed3, ed4]
    
def cnt_square(moves):
    cnt = 0
    grids, edges = gridify(moves)
    for pt in grids:
        sq_grid = square(pt)
        for s in range(4):
            if sq_grid[s] not in edges: break
            if s == 3: cnt += 1
    return cnt
