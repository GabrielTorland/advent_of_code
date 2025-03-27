



class MemorySpace
{
    public int NrRows { get; }
    public int NrCols { get; }
    public HashSet<(int, int)> CorruptBytes { get; }

    public MemorySpace(int nrRows, int nrCols)
    {
        NrRows = nrRows;
        NrCols = nrCols;
        CorruptBytes = new HashSet<(int, int)>();
    }

    public void SimulateFallingBytes(List<(int, int)> fallingBytesCoodinates, int startByte, int nrBytes)
    {
        for (int i = startByte; i < startByte + nrBytes; i++)
        {
            (int x, int y) = fallingBytesCoodinates[i];
            CorruptBytes.Add((x, y));
        }
    }
}

class Solution
{
    public Solution()
    {

    }

    int? FindShortestPath(MemorySpace memorySpace)
    {
        (int, int)[] dirs = { (1, 0), (0, 1), (-1, 0), (0, -1) };
        var queue = new PriorityQueue<(int, int, int), int>();
        queue.Enqueue((0, 0, 0), 0);
        var visited = new HashSet<(int, int)>();
        var queued = new Dictionary<(int, int), int>();

        while (queue.Count > 0)
        {
            (int x, int y, int length) = queue.Dequeue();

            visited.Add((x, y));
            queued.Remove((x, y));

            if (x == (memorySpace.NrCols - 1) && (y == memorySpace.NrRows - 1))
            {
                return length;
            }

            foreach ((int dX, int dY) in dirs)
            {
                int nextX = x + dX;
                int nextY = y + dY;

                // In bounds
                if (nextX < 0 || nextX >= memorySpace.NrCols || nextY < 0 || nextY >= memorySpace.NrRows)
                {
                    continue;
                }

                // Not visited nor corrupt
                if (visited.Contains((nextX, nextY)) || memorySpace.CorruptBytes.Contains((nextX, nextY)))
                {
                    continue;
                }

                // Not already queued with a shorter path
                if (queued.ContainsKey((nextX, nextY)) && queued[(nextX, nextY)] <= length + 1)
                {
                    continue;
                }

                queue.Enqueue((nextX, nextY, length + 1), length + 1);
                queued[(nextX, nextY)] = length + 1;
            }
        }

        return null;

    }

    List<(int, int)> GetFallingBytes(string inputFile)
    {
        var fallingBytesCoordinates = new List<(int, int)>();
        foreach (string line in File.ReadAllLines(inputFile))
        {
            int[] coordinate = line.Split(',').Select(int.Parse).ToArray();
            fallingBytesCoordinates.Add((coordinate[0], coordinate[1]));
        }
        return fallingBytesCoordinates;
    }

    public int P1(string inputFile)
    {
        var fallingBytesCoordinates = GetFallingBytes(inputFile);
        // TODO: This range seems kind of suss
        var memorySpace = new MemorySpace(71, 71);
        memorySpace.SimulateFallingBytes(fallingBytesCoordinates, 1, 1024);
        var shortestPath = FindShortestPath(memorySpace);
        if (shortestPath == null)
        {
            throw new Exception("Shortest path not found");
        }
        return shortestPath.Value;
    }

    public (int, int) P2(string inputFile)
    {
        var fallingBytesCoordinates = GetFallingBytes(inputFile);
        var memorySpace = new MemorySpace(71, 71);
        memorySpace.SimulateFallingBytes(fallingBytesCoordinates, 0, 1024);
        int i = 1025;
        do
        {
            memorySpace.SimulateFallingBytes(fallingBytesCoordinates, i, 1);
            i++;
        } while (FindShortestPath(memorySpace) != null);
        return fallingBytesCoordinates[i - 1];
    }
}

class Program
{

    static void Main(string[] args)
    {
        var solution = new Solution();
        var resultP1 = solution.P1("input");
        System.Console.WriteLine($"Part1: {resultP1}");
        var resultP2 = solution.P2("input");
        Console.WriteLine($"Part2: {resultP2.Item1},{resultP2.Item2}");
    }

}
