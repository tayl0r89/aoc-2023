
Coordinate = tuple[int,int]

def parse_exit(coordinate, pipe: str) -> list[Coordinate] | None:
    match pipe:
        case "|": return [(coordinate[0], coordinate[1] + 1), (coordinate[0], coordinate[1] - 1)]
        case "-": return [(coordinate[0] + 1, coordinate[1]), (coordinate[0] - 1, coordinate[1])]
        case "7": return [(coordinate[0] - 1, coordinate[1]), (coordinate[0], coordinate[1] + 1)]
        case "F": return [(coordinate[0] + 1, coordinate[1]), (coordinate[0], coordinate[1] + 1)]
        case "L": return [(coordinate[0] + 1, coordinate[1]), (coordinate[0], coordinate[1] - 1)]
        case "J": return [(coordinate[0] - 1, coordinate[1]), (coordinate[0], coordinate[1] - 1)]
        case "S": return [
            (coordinate[0], coordinate[1] - 1),
            (coordinate[0], coordinate[1] + 1),
            (coordinate[0] - 1, coordinate[1]),
            (coordinate[0] + 1, coordinate[1]),
        ]
        case ".": return None
    
    raise ValueError(f"{pipe} is not supported.")

def get_dir(from_node: Coordinate, to_node: Coordinate) -> str:
    if from_node[0] == to_node[0]:
        return "S" if from_node[1] < to_node[1] else "N"    
    
    return "E" if from_node[0] < to_node[0] else "W"


class Graph():

    nodes: dict[Coordinate, str]
    edges: dict[Coordinate, list[Coordinate, str]]
    start: Coordinate | None
    s_pipe: str

    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.start = None
        self.s_pipe = ""
    
    def add_node(self, coordinate: Coordinate, pipe_type: str):
        exits = parse_exit(coordinate, pipe_type)
        self.nodes[coordinate] = pipe_type
        if pipe_type == "S":
            self.start = coordinate
        
        if exits:
            for other in exits:
                if other in self.nodes:
                    other_exits = parse_exit(other, self.nodes[other])
                    if other_exits and coordinate in other_exits:
                        self.add_edge(coordinate, other)

    def add_edge(self, from_node: Coordinate, to_node: Coordinate):
        self.edges[from_node] = [*self.edges.get(from_node, []), to_node]
        self.edges[to_node] = [*self.edges.get(to_node, []), from_node]

    def get_other_edge(self, from_node: Coordinate, other_to: Coordinate):
        edge_list = self.edges.get(from_node, [])
        if len(edge_list) == 0:
            return None
        elif len(edge_list) < 2:
            raise ValueError()
        
        return edge_list[0] if edge_list[0] != other_to else edge_list[1]

    def find_loop(self):
        edges = self.edges[self.start]
        if len(edges) != 2:
            raise ValueError("Bad maze configuration")

        a_node = edges[0]
        b_node = edges[1]
        a_dir = get_dir(self.start, a_node)
        b_dir = get_dir(self.start, b_node)

        dirs = sorted([a_dir, b_dir])
        
        if dirs == ["N", "S"]:
            self.s_pipe = "|"
        elif dirs == ["E", "W"]:
            self.s_pipe = "-"
        elif dirs == ["S", "W"]:
            self.s_pipe = "7"
        elif dirs == ["E", "S"]:
            self.s_pipe = "F"
        elif dirs == ["E", "N"]:
            self.s_pipe = "J"
        elif dirs == ["N", "W"]:
            self.s_pipe = "L"
        else:
            print(dirs)


        a_path = [self.start, a_node]
        b_path = [self.start, b_node]
        a_last = self.start
        b_last = self.start

        count = 0
        
        while a_path[len(a_path) - 1] != b_path[len(b_path) - 1]:
            a_node = self.get_other_edge(a_node, a_last)
            b_node = self.get_other_edge(b_node, b_last)
            a_path.append(a_node)
            b_path.append(b_node)
            a_last = a_path[len(a_path) - 2]
            b_last = b_path[len(b_path) - 2]
            count = count + 1

        b_path.reverse()
        full_path = [*a_path, *b_path[1:]]
        return (len(a_path) - 1, full_path)

def get_nsew(pipe: str, coord: Coordinate, graph: Graph):
    match pipe:
        case "F": return "E"
        case "J": return "N"
        case "7": return "S"
        case "L": return "E"
        case "-": return "E"
        case "|": return "S"
        case "S": return graph.s_pipe
    
    raise ValueError("BAD NSEW")

def get_direction(pipe: list[str], graph: Graph, coord: Coordinate):
    first = pipe[0] if not pipe[0] == "S" else graph.s_pipe
    if len(pipe) == 1:
        match first:
            case "|": return "v"

        raise ValueError(f"BAD SINGLE PIPE {pipe[0]}")
    
    last_val = pipe[len(pipe) - 1]
    last = last_val if last_val != "S" else graph.s_pipe

    if first == "L" and last == "7":
        return "v"
    if first == "L" and last == "J":
        return "h"
    if first == "F" and last == "J":
        return "v"
    if first == "F" and last == "7":
        return "h"
    
    raise ValueError(f"BAD PIPE {first} to {last} at {coord}")

def count_closed_in_line(line: list[str], y: int, sol_graph: Graph, path: list[Coordinate]):
    enclosed_count = 0
    vert_boundaries = 0
    current_pipe = []
    for i, val in enumerate(line):
        if (i,y) in path:
            if val == "|":
                vert_boundaries = vert_boundaries + 1
            elif len(current_pipe) == 0:
                current_pipe.append(val)
            elif len(current_pipe) > 0:
                if (i,y) in sol_graph.edges[(i-1, y)]:
                    # if it connects to the current cached pipe add it
                    current_pipe.append(val)
                
                if i < len(line) - 1:
                    if (i+1, y) not in sol_graph.edges[(i,y)]:
                        pipe_dir = get_direction(current_pipe, sol_graph, (i,y))
                        if pipe_dir == "v":
                            vert_boundaries = vert_boundaries + 1
                        current_pipe = []
        else:
            if vert_boundaries > 0 and vert_boundaries % 2 == 1:
                enclosed_count = enclosed_count + 1

    return enclosed_count


if __name__ == "__main__":
    graph = Graph()
    with open("input.txt", "r", encoding="utf-8") as file:
        for y, line in enumerate(file.readlines()):
            for x, pipe in enumerate([*line.strip()]):
                    graph.add_node((x,y), pipe)
    
    loop = graph.find_loop()
    print(f"Part 1: {loop[0]}")
    to_print = []
    area_count = 0
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        output = []
        for y, line in enumerate(lines):
            output_l = []
            line_data = [*line.strip()] 
            if y == graph.start[1]:
                line_data[graph.start[0]] = graph.s_pipe
            enclosed_count = count_closed_in_line(line, y, graph, loop[1])
            area_count = area_count + enclosed_count
    
    print(f"Part 2: {area_count}")
                    

                    


                    
                    

