
class Solution
{

    public Solution()
    {

    }

    char[,] GetMap(string fileName)
    {
        var lines = File.ReadAllLines(fileName);
        int nrRows = lines.Count();
        int nrCols = lines[0].Count();
        var map = new char[nrRows, nrCols];

        for (int i = 0; i < nrRows; i++)
        {
            for (int j = 0; j < nrCols; j++)
            {
                map[i, j] = lines[i][j];
            }
        }
        return map;
    }

    IEnumerable<(int, int)> GetValuePositions(char[,] map, char target)
    {
        for (int i = 0; i < map.GetLength(0); i++)
        {
            for (int j = 0; j < map.GetLength(1); j++)
            {
                if (map[i, j] == target)
                {
                    yield return (j, i);
                }
            }
        }
    }

    List<(int, int)> GetBaselinePath(char[,] map, (int, int) startPostion, (int, int) endPosition)
    {
        var dirs = new (int, int)[] { (1, 0), (0, 1), (-1, 0), (0, -1) };
        List<(int, int)> visited = new List<(int, int)>();

        var stack = new Stack<(int, int, int)>();
        stack.Push((startPostion.Item1, startPostion.Item2, 0));

        while (stack.Count() > 0)
        {
            (int currentX, int currentY, int time) = stack.Pop();
            visited.Add((currentX, currentY));
            if ((currentX, currentY) == endPosition)
            {
                return visited;
            }

            foreach ((int dX, int dY) in dirs)
            {
                int nextX = currentX + dX;
                int nextY = currentY + dY;
                if (map[nextY, nextX] == '#' || visited.Contains((nextX, nextY)))
                {
                    continue;
                }
                stack.Push((nextX, nextY, time + 1));
            }
        }
        throw new Exception("No path found");

    }

    IEnumerable<(int, int)> GetHorizontalShortcuts(char[,] map)
    {
        var legalValues = new char[] { '.', 'S', 'E' };
        for (int i = 0; i < map.GetLength(0); i++)
        {
            for (int j = 0; j < map.GetLength(1) - 2; j++)
            {
                if (legalValues.Contains(map[i, j]) && map[i, j + 1] == '#' && legalValues.Contains(map[i, j + 2]))
                {
                    yield return (j, i);
                }
            }
        }

    }

    IEnumerable<(int, int)> GetVerticalShortcuts(char[,] map)
    {
        var legalValues = new char[] { '.', 'S', 'E' };
        for (int i = 0; i < map.GetLength(0); i++)
        {
            for (int j = 0; j < map.GetLength(1) - 2; j++)
            {
                if (legalValues.Contains(map[j, i]) && map[j + 1, i] == '#' && legalValues.Contains(map[j + 2, i]))
                {
                    yield return (i, j);
                }
            }
        }

    }

    public int P1(string inputFile)
    {
        var map = GetMap(inputFile);

        var startPosition = GetValuePositions(map, 'S').Single();
        var endPosition = GetValuePositions(map, 'E').Single();

        var path = GetBaselinePath(map, startPosition, endPosition);
        var counter = new Dictionary<int, int>();

        foreach (var horizontalShortcut in GetHorizontalShortcuts(map))
        {
            var fromIndex = path.FindIndex(position => position == horizontalShortcut);
            var toIndex = path.FindIndex(position => position == (horizontalShortcut.Item1 + 2, horizontalShortcut.Item2));
            int savedTime = Math.Abs(toIndex - fromIndex) - 2;

            if (!counter.ContainsKey(savedTime))
            {
                counter[savedTime] = 0;

            }
            counter[savedTime]++;
        }
        foreach (var verticalShortcut in GetVerticalShortcuts(map))
        {
            var fromIndex = path.FindIndex(position => position == verticalShortcut);
            var toIndex = path.FindIndex(position => position == (verticalShortcut.Item1, verticalShortcut.Item2 + 2));
            int savedTime = Math.Abs(toIndex - fromIndex) - 2;

            if (!counter.ContainsKey(savedTime))
            {
                counter[savedTime] = 0;

            }
            counter[savedTime]++;

        }

        return counter.Where(count => count.Key >= 100).Sum(count => count.Value);
    }

    public int P2(string inputFile)
    {
        var map = GetMap(inputFile);

        var startPosition = GetValuePositions(map, 'S').Single();
        var endPosition = GetValuePositions(map, 'E').Single();

        var baselinePath = GetBaselinePath(map, startPosition, endPosition);

        int maxCheatLength = 20;
        int viableCheats = 0;
        var counter = new Dictionary<int, int>();
        for (int i = 0; i < baselinePath.Count(); i++)
        {
            (int x, int y) = baselinePath[i];

            for (int nextX = x - maxCheatLength; nextX < x + maxCheatLength + 1; nextX++)
            {
                for (int nextY = y - maxCheatLength; nextY < y + maxCheatLength + 1; nextY++)
                {
                    if (nextX < 0 || nextX >= map.GetLength(1) || nextY < 0 || nextY >= map.GetLength(0))
                    {
                        continue;
                    }

                    int cheatLength = Math.Abs(nextX - x) + Math.Abs(nextY - y);

                    if (map[nextY, nextX] == '#' || cheatLength > 20)
                    {
                        continue;
                    }

                    int j = baselinePath.FindIndex(pos => pos == (nextX, nextY));
                    int savedTime = j - i - cheatLength;

                    if (savedTime >= 100)
                    {
                        viableCheats++;
                        if (!counter.ContainsKey(savedTime))
                        {
                            counter[savedTime] = 0;
                        }
                        counter[savedTime]++;
                    }
                }

            }
        }
        return viableCheats;
    }

    class Program
    {

        static void Main(string[] args)
        {
            var solution = new Solution();
            string inputFile = "input";
            System.Console.WriteLine($"Part 1: {solution.P1(inputFile)}");
            System.Console.WriteLine($"Part 2: {solution.P2(inputFile)}");
        }

    }
}
