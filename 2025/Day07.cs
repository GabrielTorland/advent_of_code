using System.Text.RegularExpressions;

namespace AdventOfCode;

public class Day07 : BaseDay
{
    private readonly char[][] _map;

    public long SimulateBeam(int i, int j, HashSet<(int i, int j)> visited)
    {
        var totalSplits = 0L;

        if (i+1 >= _map.Length || j >= _map[i].Length || j < 0)
        {
            return 0;
        }

        if (visited.Contains((i + 1, j)))
        {
            return 0;
        }

        var newSplits = 0L;
        if (_map[i+1][j] != '^')
        {
            newSplits += SimulateBeam(i + 1, j, visited);
        }
        else
        {
            newSplits++;
            newSplits += SimulateBeam(i + 1, j - 1, visited);
            newSplits += SimulateBeam(i + 1, j + 1, visited);
        }

        totalSplits += newSplits;
        visited.Add((i+1, j));

        return totalSplits;
    }

    public long SimulateBeamV2(int i, int j, Dictionary<(int i, int j), long> visited)
    {
        var timelines = 0L;

        if (i+1 == _map.Length)
        {
            return 1;
        }

        if (j >= _map[i].Length || j < 0)
        {
            return 0;
        }

        var newTimelines = 0L;
        if (visited.TryGetValue((i + 1, j), out newTimelines))
        {
            return newTimelines;
        }

        if (_map[i+1][j] != '^')
        {
            newTimelines += SimulateBeamV2(i + 1, j, visited);
        }
        else
        {
            newTimelines += SimulateBeamV2(i + 1, j - 1, visited);
            newTimelines += SimulateBeamV2(i + 1, j + 1, visited);
        }

        timelines += newTimelines;
        visited.Add((i+1, j), newTimelines);

        return timelines;
    }

public ValueTask<string> TrashP1()
    {
        var startPosition = (0, _map[0].IndexOf('S'));
        var beams = new HashSet<int>{ startPosition.Item2 };
        var splits = 0;

        for (var i = 0; i < _map.Length; i++)
        {
            for (var j = 0; j < _map[i].Length; j++)
            {
                if (_map[i][j] == '^' && beams.Contains(j))
                {
                    beams.Remove(j);
                    if (j-1 >= 0)
                    {
                        beams.Add(j-1);
                    }

                    if (j+1 < _map[i].Length)
                    {
                        beams.Add(j+1);
                    }
                    splits++;
                }
            }
        }

        return ValueTask.FromResult(splits.ToString());
    }

    public ValueTask<string> P1()
    {
        var startPosition = (0, _map[0].IndexOf('S'));
        var totalSplits = SimulateBeam(startPosition.Item1, startPosition.Item2, new HashSet<(int i, int j)>());

        return ValueTask.FromResult(totalSplits.ToString());
    }


    public ValueTask<string> P2()
    {
        var startPosition = (0, _map[0].IndexOf('S'));
        var totalTimelines = SimulateBeamV2(startPosition.Item1, startPosition.Item2, new Dictionary<(int i, int j), long>());
        return ValueTask.FromResult(totalTimelines.ToString());
    }

    public Day07()
    {
        _map = File.ReadAllLines("Inputs/07.txt").Select(line => line.ToArray()).ToArray();
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
