namespace AoC.Y2024.D10;



class Map
{
    private int[,] RawMap;
    private int Height;
    private int Width;

    public Map(int[,] rawMap)
    {
        RawMap = rawMap;
        Height = rawMap.GetLength(0);
        Width = rawMap.GetLength(1);
    }

    private bool InRange(int x, int y)
    {
        return (x >= 0 && x < Width && y >= 0 && y < Height);
    }

    public IEnumerable<(int, int, int)> GetNeighbors(int x, int y, int z)
    {
        (int, int)[] directions = { (1, 0), (0, 1), (-1, 0), (0, -1) };

        foreach ((int deltaX, int deltaY) in directions)
        {
            if (!InRange(x + deltaX, y + deltaY))
            {
                continue;
            }

            yield return (x + deltaX, y + deltaY, RawMap[y + deltaY, x + deltaX]);
        }
    }

    public IEnumerable<(int, int)> GetPossibleTrailheads()
    {
        for (int y = 0; y < Height; y++)
        {
            for (int x = 0; x < Width; x++)
            {
                if (RawMap[y, x] == 0)
                {
                    yield return (x, y);
                }
            }
        }
    }

}


class Trail
{

    public List<(int x, int y, int z)> Visited { get; set; }


    public Trail(int x, int y, int z)
    {
        Visited = new List<(int x, int y, int z)>();
        Visited.Add((x, y, z));
    }

    private Trail(List<(int x, int y, int z)> visitedList)
    {
        Visited = new List<(int x, int y, int z)>(visitedList);
    }


    public bool Contains(int x, int y, int z)
    {

        return Visited.Contains((x, y, z));
    }

    public (int x, int y, int z) GetLastVisited()
    {
        return Visited[Visited.Count - 1];
    }

    public Trail Copy()
    {
        return new Trail(this.Visited);
    }

    public Trail getNextTrail(int nextX, int nextY, int nextZ)
    {
        var nextTrail = Copy();
        nextTrail.Visited.Add((nextX, nextY, nextZ));
        return nextTrail;
    }
}


class Solution
{

    public Map GetMap(string inputFile)
    {
        string[] lines = File.ReadAllLines(inputFile);

        int height = lines.Length;
        int width = lines[0].Length;
        var rawMap = new int[height, width];

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                rawMap[y, x] = Convert.ToInt32(Char.GetNumericValue(lines[y][x]));
            }

        }
        return new Map(rawMap);

    }

    public int GetTotalTrailheadsScore(Map map)
    {
        int trailheadsScore = 0;
        foreach ((int x, int y) in map.GetPossibleTrailheads())
        {
            var queue = new Queue<(int, int, int)>();
            queue.Enqueue((x, y, 0));
            var visited = new HashSet<(int, int)>();

            while (queue.Count() != 0)
            {
                (int currentX, int currentY, int currentZ) = queue.Dequeue();

                if (visited.Contains((currentX, currentY)))
                {
                    continue;
                }
                else
                {
                    visited.Add((currentX, currentY));
                }

                if (currentZ == 9)
                {
                    trailheadsScore++;
                    continue;
                }

                foreach ((int nextX, int nextY, int nextZ) in map.GetNeighbors(currentX, currentY, currentZ))
                {
                    if ((nextZ - currentZ) != 1)
                    {
                        continue;
                    }
                    queue.Enqueue((nextX, nextY, nextZ));

                }
            }
        }
        return trailheadsScore;

    }

    public int GetTotalUniqueTrailheadsScore(Map map)
    {
        int uniqueTrailheadsScore = 0;
        foreach ((int x, int y) in map.GetPossibleTrailheads())
        {
            var queue = new Queue<Trail>();
            queue.Enqueue(new Trail(x, y, 0));

            while (queue.Count() != 0)
            {
                var currentTrail = queue.Dequeue();
                var currentPos = currentTrail.GetLastVisited();

                if (currentPos.z == 9)
                {
                    uniqueTrailheadsScore++;
                    continue;
                }

                foreach ((int nextX, int nextY, int nextZ) in map.GetNeighbors(currentPos.x, currentPos.y, currentPos.z))
                {
                    if ((nextZ - currentPos.z) != 1 || currentTrail.Contains(nextX, nextY, nextZ))
                    {
                        continue;
                    }

                    queue.Enqueue(currentTrail.getNextTrail(nextX, nextY, nextZ));
                }
            }
        }
        return uniqueTrailheadsScore;
    }

}


class Program
{

    static void Main(string[] args)
    {
        var solution = new Solution();
        Map map = solution.GetMap("input.txt");
        int totalTrailheadsScore = solution.GetTotalTrailheadsScore(map);
        Console.WriteLine($"Part 1: {totalTrailheadsScore}");
        int totalUniqueTrailheadsScore = solution.GetTotalUniqueTrailheadsScore(map);
        Console.WriteLine($"Part 2: {totalUniqueTrailheadsScore}");
    }
}
