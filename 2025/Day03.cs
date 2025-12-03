using System;

namespace AdventOfCode;

public class Day03 : BaseDay
{
    private readonly List<string> _banks = [];

    public ValueTask<string> P1()
    {
        var outputJoltage = 0;
        foreach (var bank in _banks)
        {
            var maximumJoltage = 0;
            for (int i = 0; i < bank.Count(); i++)
            {
                for (int j = i+1; j < bank.Count(); j++)
                {
                    var aJoltage = int.Parse(bank[i].ToString())*10 + int.Parse(bank[j].ToString());

                    if (aJoltage > maximumJoltage)
                    {
                        maximumJoltage = aJoltage;
                    }
                }
            }

            outputJoltage += maximumJoltage;
        }

        return ValueTask.FromResult(outputJoltage.ToString());
    }

    private long CalculateMaximumYoltage(
        string bank,
        long currentJoltage,
        long currentMaxYoltage,
        int currentIndex,
        int digitsLeft,
        Dictionary<(int, int), long> visited)
    {
        if (digitsLeft == 0)
        {
            return currentJoltage;
        }

        if (digitsLeft > bank.Length - currentIndex)
        {
            return 0;
        }

        if (visited.ContainsKey((currentIndex, digitsLeft)))
        {
            return currentJoltage + visited[(currentIndex, digitsLeft)];
        }

        var foundNewMaxYoltage = false;
        for (int i = currentIndex; i < bank.Length - digitsLeft + 1; i++)
        {
            var digit = long.Parse(bank[i].ToString());

            var nextJoltage = currentJoltage + digit*(long)Math.Pow(10, digitsLeft - 1);

            // If less than current max yoltage, prune
            if (nextJoltage < (currentMaxYoltage - currentMaxYoltage % Math.Pow(10, digitsLeft - 1)))
            {
                continue;
            }

            var aJoltage = CalculateMaximumYoltage(bank, nextJoltage, currentMaxYoltage, i + 1, digitsLeft - 1, visited);

            if (aJoltage > currentMaxYoltage)
            {
                currentMaxYoltage = aJoltage;
                foundNewMaxYoltage = true;
            }
        }

        if (foundNewMaxYoltage)
        {
            visited.Add((currentIndex, digitsLeft), currentMaxYoltage % (long)Math.Pow(10, digitsLeft));
        }

        return currentMaxYoltage;
    }


    public ValueTask<string> P2()
    {
        long outputJoltage = 0;
        foreach (var bank in _banks)
        {
            outputJoltage += CalculateMaximumYoltage(bank, 0, 0, 0, 12, new Dictionary<(int, int), long>());
        }

        return ValueTask.FromResult(outputJoltage.ToString());
    }

    public Day03()
    {
        foreach (var line in File.ReadAllLines("Inputs/03.txt"))
        {
            _banks.Add(line);
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
