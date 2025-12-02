using System;

namespace AdventOfCode;

public class Day02 : BaseDay
{
    private readonly List<(string, string)> _ranges = [];

    private bool IsInvalid(string number)
    {
        var leftNumber = long.Parse(number.Substring(0, number.Length/2));
        var rightNumber = long.Parse(number.Substring(number.Length/2, number.Length/2));

        return leftNumber == rightNumber;
    }

    public ValueTask<string> P1()
    {
        var invalidIds = new List<long>();

        foreach (var (start, end) in _ranges)
        {
            var currentNumber = long.Parse(start);
            var lastNumber = long.Parse(end);
            var delta = 1L;
            while (currentNumber <= lastNumber)
            {
                var currentNumberStr = currentNumber.ToString();

                if (currentNumberStr.Length % 2 == 0 && IsInvalid(currentNumberStr))
                {
                    delta = (long)Math.Pow(10, currentNumberStr.Length/2)+1;
                    invalidIds.Add(currentNumber);
                }
                else if (delta > 1)
                {
                    currentNumber -= delta;
                    delta = 1;
                }

                currentNumber += delta;
            }
        }

        return ValueTask.FromResult(invalidIds.Sum().ToString());
    }

    private bool IsInvalidV2(string number)
    {
        var isInvalid = false;
        for (int n = 1; n <= number.Length/2; n++)
        {
            var part = number.Substring(0, n);

            if ((number.Length - n) % n != 0)
            {
                continue;
            }

            isInvalid = true;
            for (int i = n; i < number.Length; i += n)
            {
                var otherPart = number.Substring(i, n);

                if (otherPart != part)
                {
                    isInvalid = false;
                    break;
                }
            }

            if (isInvalid == true)
            {
                return isInvalid;
            }
        }

        return isInvalid;
    }

    public ValueTask<string> P2()
    {
        var invalidIds = new List<long>();

        foreach (var (start, end) in _ranges)
        {
            var currentNumber = long.Parse(start);
            var lastNumber = long.Parse(end);
            while (currentNumber <= lastNumber)
            {
                if (IsInvalidV2(currentNumber.ToString()))
                {
                    invalidIds.Add(currentNumber);
                }

                currentNumber++;
            }
        }

        return ValueTask.FromResult(invalidIds.Sum().ToString());
    }

    public Day02()
    {
        foreach (var line in File.ReadAllText("Inputs/02.txt").Split(','))
        {
            var range = line.Split("-");
            _ranges.Add((range.First(), range.Last()));
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
