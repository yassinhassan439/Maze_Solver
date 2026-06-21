import random


class Maze:
    def __init__(self, maze_grid=None):
        self.maze = maze_grid
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.start = self.find_position('S')
        self.end = self.find_position('E')

    def find_position(self, symbol):
        """Find the position of a symbol (S or E) in the maze"""
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == symbol:
                    return (i, j)
        return None

    def print_maze(self, path=None, visited=None):
        """Print the maze with path and visited cells"""
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                pos = (i, j)
                if cell in ['S', 'E']:
                    print(cell, end=' ')
                elif path and pos in path:
                    print('*', end=' ')
                elif visited and pos in visited:
                    print('.', end=' ')
                else:
                    print(cell, end=' ')
            print()
        print()


def dfs_solve(maze, start, end):
    """
    Solve maze using Depth-First Search with backtracking
    Uses iterative approach with explicit stack
    """
    visited = set()
    stack = [(start, [start])]  # (position, path_to_position)

    while stack:
        (row, col), path = stack.pop()

        # Skip if already visited
        if (row, col) in visited:
            continue

        # Skip if out of bounds
        if not (0 <= row < maze.height and 0 <= col < maze.width):
            continue

        # Skip if wall
        if maze.maze[row][col] == '#':
            continue

        # Mark as visited
        visited.add((row, col))

        # Check if we found the end
        if (row, col) == end:
            return path, visited

        # Add neighbors to stack (in reverse order for correct DFS priority)
        for dr, dc in [(-1, 0), (0, 1), (0, -1), (1, 0)]:  # Up, Right, Left, Down
            new_pos = (row + dr, col + dc)
            new_path = path + [new_pos]
            stack.append((new_pos, new_path))

    return None, visited

def build_graph(maze):
    """
    Convert maze into a graph representation
    Returns adjacency list showing connections between cells
    """
    graph = {}

    for row in range(maze.height):
        for col in range(maze.width):
            # Only add non-wall cells to graph
            if maze.maze[row][col] != '#':
                neighbors = []

                # Check all 4 directions
                directions = [(1,0), (0,-1), (0,1), (-1,0)]  #  Down, Left,Right, Up,

                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc

                    # If neighbor is valid and not a wall, add connection
                    if (0 <= new_row < maze.height and
                            0 <= new_col < maze.width and
                            maze.maze[new_row][new_col] != '#'):
                        neighbors.append((new_row, new_col))

                graph[(row, col)] = neighbors

    return graph


def print_graph(graph, maze):
    """Print the graph in a readable format"""
    print("\nGRAPH REPRESENTATION (Adjacency List):")
    print("=" * 60)
    print("Each cell shows its connections to neighboring cells\n")

    for node, neighbors in sorted(graph.items()):
        row, col = node
        cell_type = maze.maze[row][col]

        if cell_type == 'S':
            label = f"START {node}"
        elif cell_type == 'E':
            label = f"END   {node}"
        else:
            label = f"Cell  {node}"

        print(f"{label} → connects to: {neighbors}")

    print(f"\nTotal nodes (cells): {len(graph)}")
    total_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    print(f"Total edges (connections): {total_edges}")


def main():
    print("MAZE SOLVER USING DFS")
    print("=" * 40)

    # Example: You can easily change the maze here or pass your own

        # [
        #     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        #     ['#', 'S', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', ' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#'],
        #     ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
        #     ['#', ' ', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
        #     ['#', '#', '#', ' ', '#', '#', '#', ' ', '#', 'E', '#'],
        #     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        # ]
    custom_maze = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', 'S', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
        ['#', '#', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
        ['#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', 'E', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
    ]

    # Create maze with custom input
    maze = Maze(custom_maze)

    print(f"\nMaze size: {maze.height} rows × {maze.width} columns")
    print(f"Start position: {maze.start}")
    print(f"End position: {maze.end}")

    print("\nOriginal Maze:")
    print("S = Start, E = End, # = Wall\n")
    maze.print_maze()

    # Build and show the graph
    graph = build_graph(maze)
    print_graph(graph, maze)

    print("\n" + "=" * 60)
    print("\nNow solving with DFS algorithm using this graph...")
    solution, visited = dfs_solve(maze, maze.start, maze.end)

    if solution:
        print(f"\nSolution found!")
        print(f"Path length: {len(solution)} steps")
        print(f"Total cells visited: {len(visited)}")
        print("\nLegend: S=Start, E=End, *=Solution path, .=Visited but not in solution\n")
        maze.print_maze(path=solution, visited=visited)

        # print("\nSolution path coordinates:")
        # for i, pos in enumerate(solution):
        #     print(f"Step {i}: {pos}")
    else:
        print("No solution found!")


if __name__ == "__main__":
    main()