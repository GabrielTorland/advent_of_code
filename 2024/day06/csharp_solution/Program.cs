
namespace Day6
{
    class InputParser
    {
        public static char[,] Parse(string inputFile)
        {
            string[] lines = File.ReadAllLines(inputFile);
            int nrRows = lines.Length;
            int nrCols = lines[0].Length;
            char[,] map = new char[nrRows, nrCols];
            for (int i = 0; i < nrRows; i++)
            {
                for (int j = 0; j < nrCols; j++)
                {
                    map[i, j] = lines[i][j];
                }
            }
            return map;
        }
    }

    class Simulator
    {

        private char[,] Map { get; set; }
        private int NrRows { get; }
        private int NrCols { get; }
        private (int GuardRow, int GuardCol) GuardPosition { get; set; }
        private Dictionary<char, (int di, int dj)> DirectionOffsets { get; }

        public Simulator(char[,] map)
        {
            Map = map;
            NrRows = map.GetLength(0);
            NrCols = map.GetLength(1);
            GuardPosition = getGuardPosition();
            DirectionOffsets = new Dictionary<char, (int di, int dj)>
            {
                ['>'] = (0, 1),
                ['v'] = (1, 0),
                ['<'] = (0, -1),
                ['^'] = (-1, 0)
            };
        }

        private (int, int) getGuardPosition()
        {
            for (int i = 0; i < NrRows; i++)
            {
                for (int j = 0; j < NrCols; j++)
                {
                    if (new[] { '>', '<', '^', 'v' }.Contains(Map[i, j]))
                    {
                        return (i, j);
                    }
                }
            }
            throw new InvalidOperationException("No guard position ('O') found in the map!");
        }
        public int Run()
        {

            (int di, int dj)[] directionVectors = DirectionOffsets.Values.ToArray();

            (int i, int j) = GuardPosition;
            char guardDirection = Map[GuardPosition.GuardRow, GuardPosition.GuardCol];

            (int currentDi, int currentDj) = DirectionOffsets[guardDirection];
            int dirIndex = Array.FindIndex(directionVectors, v => v.di == currentDi && v.dj == currentDj);

            bool insideMap = true;
            var visited = new HashSet<(int, int)>();
            visited.Add((i, j));
            while (insideMap)
            {
                (int nextI, int nextJ) = (i + currentDi, j + currentDj);
                if (nextI < 0 || nextI >= NrRows || nextJ < 0 || nextJ >= NrCols)
                {
                    insideMap = false;
                }
                else if (Map[nextI, nextJ] == '#')
                {
                    dirIndex = (dirIndex + 1) % 4;
                    (currentDi, currentDj) = directionVectors[dirIndex];
                }
                else
                {
                    i = nextI;
                    j = nextJ;
                    visited.Add((i, j));
                }
            }
            return visited.Count;
        }

        public int FindLoops()
        {
            var loopObstacles = new HashSet<(int, int)>();
            (int di, int dj)[] directionVectors = DirectionOffsets.Values.ToArray();

            (int i, int j) = GuardPosition;
            char guardDirection = Map[GuardPosition.GuardRow, GuardPosition.GuardCol];

            (int currentDi, int currentDj) = DirectionOffsets[guardDirection];
            int dirIndex = Array.FindIndex(directionVectors, v => v.di == currentDi && v.dj == currentDj);
            PlacedObstacle? placedObstacle = null;
            bool insideMap = true;
            var visited = new HashSet<(int, int, int)>();
            var tmpVisited = new HashSet<(int, int, int)>();
            while (insideMap)
            {
                (int nextI, int nextJ) = (i + currentDi, j + currentDj);

                if (nextI < 0 || nextI >= NrRows || nextJ < 0 || nextJ >= NrCols)
                {
                    if (placedObstacle == null)
                    {
                        insideMap = false;
                    }
                    else
                    {
                        i = placedObstacle.I;
                        j = placedObstacle.J;
                        Map[i, j] = '.';
                        dirIndex = placedObstacle.DirIndex;
                        (currentDi, currentDj) = directionVectors[dirIndex];
                        placedObstacle = null;
                        visited.Add((i, j, dirIndex));
                    }
                }
                else if (Map[nextI, nextJ] == '#')
                {
                    dirIndex = (dirIndex + 1) % 4;
                    (currentDi, currentDj) = directionVectors[dirIndex];
                }
                else if (!visited.Any(v => v.Item1 == nextI && v.Item2 == nextJ) && placedObstacle == null)
                {
                    placedObstacle = new PlacedObstacle(nextI, nextJ, dirIndex);
                    tmpVisited = new HashSet<(int, int, int)>();
                    Map[nextI, nextJ] = '#';
                }

                else
                {
                    i = nextI;
                    j = nextJ;
                    if (visited.Contains((i, j, dirIndex)) || tmpVisited.Contains((i, j, dirIndex)))
                    {
                        i = placedObstacle.I;
                        j = placedObstacle.J;
                        Map[i, j] = '.';
                        dirIndex = placedObstacle.DirIndex;
                        (currentDi, currentDj) = directionVectors[dirIndex];
                        placedObstacle = null;
                        loopObstacles.Add((i, j));
                    }
                    if (placedObstacle == null)
                    {
                        visited.Add((i, j, dirIndex));
                    }
                    else
                    {
                        tmpVisited.Add((i, j, dirIndex));
                    }
                }

            }
            return loopObstacles.Count;
        }
    }
    class PlacedObstacle
    {
        public int I { get; }
        public int J { get; }
        public int DirIndex { get; }

        public PlacedObstacle(int i, int j, int dirIndex)
        {
            I = i;
            J = j;
            DirIndex = dirIndex;
        }


    }
    class Program
    {
        static void Main(string[] args)
        {
            char[,] map = InputParser.Parse("input.txt");
            var simulator = new Simulator(map);
            int uniquePositions = simulator.Run();
            Console.WriteLine($"Part 1: {uniquePositions}");
            int nrLoops = simulator.FindLoops();
            Console.WriteLine($"Part 2: {nrLoops}");
        }
    }
}
