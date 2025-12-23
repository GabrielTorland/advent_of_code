using System.Text.RegularExpressions;

namespace AdventOfCode;

public class Day12 : BaseDay
{
    private readonly List<Present> _presents = new();
    private readonly List<Floor> _floors = new();

    public ValueTask<string> P1()
    {
        var invalidFloors = 0;
        foreach (var floor in _floors)
        {
            var floorArea = floor.GetArea();
            var presentArea = 0;

            for (int i = 0; i < _presents.Count(); i++)
            {
                presentArea += _presents[i].GetArea()*floor.PresentCounts[i];
            }

            if (floorArea < presentArea)
            {
                invalidFloors++;
                continue;
            }
        }
        return ValueTask.FromResult("hi mom");
    }

    public ValueTask<string> P2()
    {
        return ValueTask.FromResult("hi mom");
    }

    private class Floor(int height, int width, int[] presentCounts)
    {
        public int[] PresentCounts { get; set; } = presentCounts;

        public int GetArea()
        {
            return (height)*(width);
        }
    }

    private class Present(HashSet<(int, int)> points)
    {
        public int GetArea()
        {
            return points.Count();
        }
    }


    public Day12()
    {
        var rawInput = File.ReadAllText("Inputs/12.txt")
            .Split($"{Environment.NewLine}{Environment.NewLine}")
            .ToArray();

        for (int i = 0; i < rawInput.Length - 1; i++)
        {
            var lines = rawInput[i].Split().ToArray();
            var points = new HashSet<(int, int)>();
            for (int j = 1; j < lines.Length; j++)
            {
                var aLine = lines[j];
                var xs = Enumerable.Range(0, aLine.Count())
                    .Where(k => aLine[k] == '#');

                foreach (var x in xs)
                {
                    points.Add((j, x));
                }
            }

            _presents.Add(new Present(points));
        }

        foreach (var line in rawInput.Last().TrimEnd().Split("\n"))
        {
            var match = Regex.Match(line, @"(\d+)x(\d+)");
            var height = int.Parse(match.Groups[1].Value);
            var width = int.Parse(match.Groups[2].Value);

            var presentCounts = line
                .Split(": ")
                .Last()
                .Trim()
                .Split(" ")
                .Select(int.Parse)
                .ToArray();

            _floors.Add(new Floor(height, width, presentCounts));
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
