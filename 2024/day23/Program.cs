using QuikGraph;


class Solution
{
    UndirectedGraph<string, Edge<string>> GetGraph(string inputFile)
    {
        var graph = new UndirectedGraph<string, Edge<string>>(allowParallelEdges: false);
        foreach (var line in File.ReadAllLines(inputFile))
        {
            var vertices = line.Split('-');
            graph.AddVertex(vertices[0]);
            graph.AddVertex(vertices[1]);
            graph.AddEdge(new Edge<string>(vertices[0], vertices[1]));
        }
        return graph;
    }

    IEnumerable<HashSet<string>> FindLans(UndirectedGraph<string, Edge<string>> graph, string currentVertex, HashSet<string> exhaustedVertices, HashSet<string> lan, HashSet<(string, string)> visitedEdges, int minSize, int maxSize)
    {

        foreach (var adjVertex in graph.AdjacentVertices(currentVertex))
        {
            if (exhaustedVertices.Contains(adjVertex) || visitedEdges.Contains((currentVertex, adjVertex)) || lan.Contains(adjVertex))
            {
                continue;
            }

            visitedEdges.Add((currentVertex, adjVertex));
            visitedEdges.Add((adjVertex, currentVertex));

            var secondAdjacentVertices = graph.AdjacentVertices(adjVertex);

            bool isValid = true;
            foreach (var vertex in lan)
            {
                if (!secondAdjacentVertices.Contains(vertex))
                {
                    isValid = false;
                    break;

                }
            }
            if (!isValid)
            {
                continue;
            }

            var nextLan = new HashSet<string>(lan);
            nextLan.Add(adjVertex);
            if (nextLan.Count >= minSize && nextLan.Count <= maxSize && nextLan.Any(v => v.StartsWith("t")))
            {
                yield return nextLan;
            }
            if (nextLan.Count < maxSize)
            {
                foreach (var foundLan in FindLans(graph, adjVertex, exhaustedVertices, nextLan, visitedEdges, minSize, maxSize))
                {
                    yield return foundLan;
                }
            }

        }
    }

    IEnumerable<HashSet<string>> GetLans(UndirectedGraph<string, Edge<string>> graph, int minSize, int maxSize)
    {
        var exhaustedVertices = new HashSet<string>();

        foreach (var currentVertex in graph.Vertices)
        {
            foreach (var lan in FindLans(graph, currentVertex, exhaustedVertices,
                        new HashSet<string>() { currentVertex }, new HashSet<(string, string)>(), minSize, maxSize))
            {
                yield return lan;
            }
            exhaustedVertices.Add(currentVertex);
        }
    }


    public int P1(string inputFile)
    {
        var graph = GetGraph(inputFile);
        return GetLans(graph, 3, 3).Count();
    }

    public string P2(string inputFile)
    {
        var graph = GetGraph(inputFile);
        var largestLan = GetLans(graph, 3, int.MaxValue).OrderByDescending(s => s.Count).First();
        return string.Join(',', largestLan.OrderBy(pc => pc));
    }

}

class Program
{
    static void Main(string[] args)
    {
        string inputFile = "input";
        var solution = new Solution();
        System.Console.WriteLine($"Part 1: {solution.P1(inputFile)}");
        System.Console.WriteLine($"Part 2: {solution.P2(inputFile)}");
    }

}
