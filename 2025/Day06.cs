using System.Text.RegularExpressions;

namespace AdventOfCode;

public class Day06 : BaseDay
{
    private readonly List<int[]> _numbers = new();
    private readonly string[] _symbols;

    public ValueTask<string> P1()
    {
        int i = 0;
        long result = 0;
        foreach (var numbers in _numbers)
        {
            var symbol = _symbols[i];

            switch (symbol)
            {
                case "+":
                    result += numbers.Sum();
                    break;
                case "*":
                    var temp = 1L;
                    foreach (var number in numbers)
                    {
                        temp *= number;
                    }
                    result += temp;
                    break;
                default:
                    throw new InvalidOperationException("This should not happen!");
            }
            i++;
        }

        return ValueTask.FromResult(result.ToString());
    }


    public ValueTask<string> P2()
    {
        var map = File.ReadAllText("Inputs/06.txt").TrimEnd().Split("\n").ToList();
        map.Remove(map.Last());

        var pattern = new Regex(@"\d+", RegexOptions.Compiled);


        var matches = new List<MatchCollection>();
        foreach (var row in map)
        {
            matches.Add(pattern.Matches(row));
        }


        var result = 0L;
        for (var j = 0; j < matches[0].Count(); j++)
        {
            var numbers = new List<Match>();
            for (var i = 0; i < matches.Count(); i++)
            {
                numbers.Add(matches[i][j]);
            }

            var newNumbers = new Dictionary<int, string>();
            var lineNumber = 0;
            foreach (var number in numbers)
            {
                for (var k = number.Index; k < number.Index + number.Length; k++)
                {
                    if (!newNumbers.ContainsKey(k))
                    {
                        newNumbers[k] = map[lineNumber][k].ToString();
                        continue;
                    }

                    newNumbers[k] += map[lineNumber][k].ToString();
                }
                lineNumber++;
            }

            if (_symbols[j] == "+")
            {
                result += newNumbers.Values.Select(long.Parse).Sum();
            }
            else
            {
                var subResult = 1L;
                foreach (var number in newNumbers.Values)
                {
                    subResult *= long.Parse(number);
                }
                result += subResult;
            }

        }

        return ValueTask.FromResult(result.ToString());
    }

    public Day06()
    {
        var raw = File.ReadAllText("Inputs/06.txt").TrimEnd().Split("\n").ToList();
        _symbols = raw.Last().Split().Where(symbol => symbol != string.Empty).ToArray();
        raw.Remove(raw.Last());

        var allNumbers = raw.Select(row => row.Split().Where(number => number != string.Empty).Select(int.Parse).ToArray()).ToArray();

        for (int i = 0; i < _symbols.Length; i++)
        {
            var numbers = new List<int>();
            for (int j = 0; j < allNumbers.Count(); j++)
            {
                numbers.Add(allNumbers[j][i]);
            }
            _numbers.Add(numbers.ToArray());
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
