using System;

namespace AdventOfCode;

public class Day05 : BaseDay
{
    private readonly List<(long, long)> _ranges = [];
    private readonly List<long> _ingredientIds = [];

    public ValueTask<string> P1()
    {
        var freshIngredients = 0;
        foreach (var ingrediantId in _ingredientIds)
        {
            foreach (var range in _ranges)
            {
                if (ingrediantId >= range.Item1 && ingrediantId <= range.Item2)
                {
                    freshIngredients++;
                    break;
                }
            }
        }

        return ValueTask.FromResult(freshIngredients.ToString());
    }


    public ValueTask<string> P2()
    {
        var mergedRanges = new List<(long, long)>();
        while (_ranges.Count() > 0)
        {
            var aRange = _ranges.First();
            _ranges.RemoveAt(0);
            int i = 0;
            while (i < _ranges.Count())
            {
                var otherRange = _ranges[i];
                if (aRange.Item1 < otherRange.Item1 && aRange.Item2 >= otherRange.Item1 && aRange.Item2 <= otherRange.Item2)
                {
                    aRange = (aRange.Item1, otherRange.Item2);
                    _ranges.RemoveAt(i);
                    i = -1;
                }
                else if (aRange.Item1 >= otherRange.Item1 && aRange.Item2 <= otherRange.Item2)
                {
                    aRange = (otherRange.Item1, otherRange.Item2);
                    _ranges.RemoveAt(i);
                    i = -1;
                }
                else if (aRange.Item1 >= otherRange.Item1 && aRange.Item1 <= otherRange.Item2 && aRange.Item2 > otherRange.Item2)
                {
                    aRange = (otherRange.Item1, aRange.Item2);
                    _ranges.RemoveAt(i);
                    i = -1;
                }
                else if (aRange.Item1 < otherRange.Item1 && aRange.Item2 > otherRange.Item2)
                {
                    _ranges.RemoveAt(i);
                    i = -1;
                }

                i++;
            }

            mergedRanges.Add(aRange);
        }

        var freshIngrediants = 0L;
        foreach (var mergedRange in mergedRanges)
        {
            freshIngrediants += mergedRange.Item2 - mergedRange.Item1 + 1;
        }

        return ValueTask.FromResult(freshIngrediants.ToString());
    }

    public Day05()
    {
        var raw = File.ReadAllText("Inputs/05.txt");
        var separatedData = raw.Split("\n\n");

        foreach (var rangeRaw in separatedData[0].Split("\n"))
        {
            var range = rangeRaw.Split("-");

            var start = long.Parse(range[0]);
            var end = long.Parse(range[1]);

            _ranges.Add((start, end));
        }

        foreach (var ingredientId in separatedData[1].TrimEnd().Split("\n"))
        {
            _ingredientIds.Add(long.Parse(ingredientId));
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
