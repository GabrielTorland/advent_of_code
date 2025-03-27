


class Solution
{

    (HashSet<string>, List<string>) GetTowels(string inputFile)
    {
        HashSet<string> availableTowels = new HashSet<string>();

        foreach (string towel in File.ReadAllText(inputFile).Split("\n\n")[0].Split(", "))
        {
            if (String.IsNullOrEmpty(towel))
            {
                continue;
            }
            availableTowels.Add(towel);
        }

        List<string> targetPatterns = new List<string>();
        foreach (string targetPattern in File.ReadAllText(inputFile).Split("\n\n")[1].Split('\n'))
        {
            if (String.IsNullOrEmpty(targetPattern))
            {
                continue;
            }
            targetPatterns.Add(targetPattern);
        }

        return (availableTowels, targetPatterns);
    }

    bool CompareStrings(string str1, string str2)
    {
        for (int i = 0; i < Math.Min(str1.Length, str2.Length); i++)
        {
            if (str1[i] != str2[i])
            {
                return false;
            }
        }
        return true;
    }

    IEnumerable<string> GetSubPatterns(string targetPattern, string currentTowel, HashSet<string> availableTowels)
    {
        for (int count = 1; count <= targetPattern.Count() - currentTowel.Count(); count++)
        {
            string subPattern = targetPattern.Substring(currentTowel.Count(), count);
            if (availableTowels.Contains(subPattern))
            {
                yield return subPattern;
            }
        }
    }

    bool IsPossiblePattern(string targetPattern, HashSet<string> availableTowels)
    {
        Stack<string> stack = new Stack<string>();

        var visited = new HashSet<(string, int)>();

        // initialize stack
        foreach (string subPattern in GetSubPatterns(targetPattern, "", availableTowels))
        {
            stack.Push(subPattern);
            visited.Add((subPattern, 0));
        }

        while (stack.Count > 0)
        {
            var currentTowel = stack.Pop();

            if (currentTowel.Count() == targetPattern.Count())
            {
                return true;
            }

            foreach (string subPattern in GetSubPatterns(targetPattern, currentTowel, availableTowels))
            {
                if (visited.Contains((subPattern, currentTowel.Count())))
                {
                    continue;
                }
                stack.Push(currentTowel + subPattern);
                visited.Add((subPattern, currentTowel.Count()));
            }
        }

        return false;
    }

    long GetAllPossibleSolutions(string currentTowel, string targetPattern, HashSet<string> availableTowels, Dictionary<(string, int), long> visited)
    {
        long nrSolutions = 0;

        if (currentTowel.Count() == targetPattern.Count())
        {
            return 1;
        }

        foreach (string subPattern in GetSubPatterns(targetPattern, currentTowel, availableTowels))
        {
            int i = currentTowel.Count();
            if (visited.ContainsKey((subPattern, i)))
            {
                nrSolutions += visited[(subPattern, i)];
            }
            else
            {
                long solutionsFound = GetAllPossibleSolutions(currentTowel + subPattern, targetPattern, availableTowels, visited);
                visited[(subPattern, i)] = solutionsFound;
                nrSolutions += solutionsFound;
            }
        }

        return nrSolutions;
    }

    public int P1(string inputFile)
    {
        (var availableTowels, var targetPatterns) = GetTowels(inputFile);

        int count = 0;

        foreach (string targetPattern in targetPatterns)
        {
            count += IsPossiblePattern(targetPattern, availableTowels) ? 1 : 0;
        }

        return count;
    }

    public long P2(string inputFile)
    {
        (var availableTowels, var targetPatterns) = GetTowels(inputFile);

        long nrSolutions = 0;
        foreach (string targetPattern in targetPatterns)
        {
            nrSolutions += GetAllPossibleSolutions("", targetPattern, availableTowels, new Dictionary<(string, int), long>());
        }
        return nrSolutions;
    }


}

class Program
{
    static void Main(string[] args)
    {
        Solution solution = new Solution();
        string inputFile = "input";

        Console.WriteLine($"Part 1: {solution.P1(inputFile)}");
        Console.WriteLine($"Part 2: {solution.P2(inputFile)}");
    }
}


