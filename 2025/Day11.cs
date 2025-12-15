using ScottPlot;

namespace AdventOfCode;

public class Day11 : BaseDay
{
    private readonly Dictionary<string, string[]> _map = new();
    private readonly Dictionary<(bool, bool, string), long> _cache = new();

    public int GetValidPaths(string current)
    {
        if (current == "out")
        {
            return 1;
        }

        var result = 0;
        foreach (var next in _map[current])
        {
            result += GetValidPaths(next);
        }

        return result;
    }

    public ValueTask<string> P1()
    {
        return ValueTask.FromResult(GetValidPaths("you").ToString());
    }

    public ValueTask<string> P2()
    {
        return ValueTask.FromResult(GetValidPathsV2("svr", new()).ToString());
    }


    public long GetValidPathsV2(string current, HashSet<string> visited)
    {
        var containsDAC = visited.Contains("dac");
        var containsFFT = visited.Contains("fft");

        if (current == "out")
        {
            return (containsDAC && containsFFT) ? 1 : 0;
        }

        var result = 0L;
        foreach (var next in _map[current])
        {
            if (_cache.TryGetValue((containsDAC, containsFFT, next), out var tempResult))
            {
                result += tempResult;
                continue;
            }

            var nextVisited = visited.Select(item => item).ToHashSet();
            nextVisited.Add(next);

            tempResult = GetValidPathsV2(next, nextVisited);
            _cache[(containsDAC, containsFFT, next)] = tempResult;
            result += tempResult;
        }

        return result;
    }

    public Day11()
    {
        foreach (var line in File.ReadLines("Inputs/11.txt"))
        {
            var segments = line.Split(": ");
            var key = segments.First();
            var value = segments.Last().Split(" ").ToArray();
            _map[key] = value;
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
