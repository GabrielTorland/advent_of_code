using System.Numerics;

public enum KeypadType
{
    Numpad,
    Arrowpad
}

public enum Directions
{
    X,
    Y
}


public static class KeypadMaps
{
    public static readonly Dictionary<char, Complex> NumpadMap = new Dictionary<char, Complex>
    {
        { '7', new Complex(0, 0) },
        { '8', new Complex(1, 0) },
        { '9', new Complex(2, 0) },
        { '4', new Complex(0, 1) },
        { '5', new Complex(1, 1) },
        { '6', new Complex(2, 1) },
        { '1', new Complex(0, 2) },
        { '2', new Complex(1, 2) },
        { '3', new Complex(2, 2) },
        { '0', new Complex(1, 3) },
        { 'A', new Complex(2, 3) }
    };

    public static readonly Dictionary<char, Complex> ArrowpadMap = new Dictionary<char, Complex>
    {
        { '^', new Complex(1, 0) },
        { 'A', new Complex(2, 0) },
        { '<', new Complex(0, 1) },
        { 'v', new Complex(1, 1) },
        { '>', new Complex(2, 1) }
    };

    public static Dictionary<char, Complex> GetPad(KeypadType type)
    {
        switch (type)
        {
            case KeypadType.Numpad:
                return NumpadMap;
            case KeypadType.Arrowpad:
                return ArrowpadMap;
            default:
                throw new InvalidOperationException("Invalid keypad type.");
        }
    }
}

class Solution
{
    IEnumerable<string> GetCodes(string inputFile)
    {
        foreach (string line in File.ReadAllLines(inputFile))
        {
            yield return line;
        }
    }


    List<List<int>> GetKCombs(List<int> list, int k)
    {
        var results = new List<List<int>>();

        if (k == 0)
        {
            results.Add(new List<int>());
            return results;
        }

        Combine(list, 0, new List<int>(), k, results);

        return results;
    }

    void Combine(List<int> list, int start, List<int> current, int n, List<List<int>> results)
    {
        if (n == 0)
        {
            results.Add(new List<int>(current));
        }

        for (int i = start; i < list.Count; i++)
        {
            current.Add(list[i]);
            Combine(list, i + 1, current, n - 1, results);
            current.RemoveAt(current.Count - 1);
        }
    }

    IEnumerable<string> GetShortestPaths(Dictionary<char, Complex> pad, char source, char target)
    {

        var dirVectors = new Dictionary<char, Complex>
        {
            { '>', new Complex(1, 0) },
            { 'v', new Complex(0, 1) },
            { '<', new Complex(-1, 0)},
            { '^', new Complex(0, -1)}
        };

        var dirVector = (pad[target] - pad[source]);
        int distanceX = (int)Math.Abs(dirVector.Real);
        int distanceY = (int)Math.Abs(dirVector.Imaginary);
        int totalDistance = distanceX + distanceY;

        if (totalDistance == 0)
        {
            yield return "A";
            yield break;
        }

        var dirX = dirVector.Real switch
        {
            0 => ' ',
            > 0 => '>',
            < 0 => '<',
            _ => throw new InvalidOperationException($"Unexpected value for dirVector.Real: {dirVector.Imaginary}")
        };

        var dirY = dirVector.Imaginary switch
        {
            0 => ' ',
            > 0 => 'v',
            < 0 => '^',
            _ => throw new InvalidOperationException($"Unexpected value for dirVector.Imaginary: {dirVector.Imaginary}")
        };

        foreach (var comb in GetKCombs(Enumerable.Range(0, totalDistance).ToList(), distanceY))
        {
            var instructions = new string(dirX, totalDistance).ToCharArray();
            foreach (var i in comb)
            {
                instructions[i] = dirY;
            }

            // validate instructions combo
            var currentPosition = pad[source];
            bool isValid = true;
            foreach (var instruction in instructions)
            {
                currentPosition += dirVectors[instruction];
                if (!pad.ContainsValue(currentPosition))
                {
                    isValid = false;
                    break;
                }
            }

            if (!isValid)
            {
                continue;
            }

            yield return new string(instructions) + "A";
        }

    }

    long GetMinimalCost(KeypadType keypadType, char source, char target, int layer, Dictionary<(char, char, int), long> cache)
    {
        var pad = KeypadMaps.GetPad(keypadType);
        if (layer == 0)
        {
            return GetShortestPaths(pad, source, target).Min(s => s.Length);
        }
        long minCost = long.MaxValue;
        foreach (string currentInstructions in GetShortestPaths(pad, source, target))
        {
            long currentCost = 0;
            char currentPosition = 'A';
            foreach (char subTarget in currentInstructions)
            {
                long cost;
                var key = (currentPosition, subTarget, layer - 1);
                if (!cache.TryGetValue(key, out cost))
                {
                    cost = GetMinimalCost(KeypadType.Arrowpad, currentPosition, subTarget, layer - 1, cache);
                    cache[key] = cost;
                }
                currentCost += cost;
                currentPosition = subTarget;
            }
            minCost = Math.Min(currentCost, minCost);
        }
        return minCost;
    }

    List<string> GetPossibleInstructions(Dictionary<char, Complex> pad, string target)
    {
        List<string> instructions = new List<string> { "" };
        var currentPosition = 'A';
        foreach (char subTarget in target)
        {
            var currentInstructions = GetShortestPaths(pad, currentPosition, subTarget);
            instructions = instructions.SelectMany(
                    s1 => currentInstructions,
                    (s1, s2) => s1 + s2
                    ).ToList();
            currentPosition = subTarget;
        }
        return instructions;
    }

    public int P1(string inputFile)
    {
        int complexitySum = 0;
        foreach (string code in GetCodes(inputFile))
        {
            var pad = KeypadMaps.GetPad(KeypadType.Numpad);
            var firstInstructions = GetPossibleInstructions(pad, code);


            pad = KeypadMaps.GetPad(KeypadType.Arrowpad);
            var currentInstructions = firstInstructions;
            var cache = new Dictionary<(char, char), IEnumerable<string>>();
            for (int i = 0; i < 2; i++)
            {
                List<string> nextInstruction = new List<string>();
                foreach (string instruction in currentInstructions)
                {
                    nextInstruction.AddRange(GetPossibleInstructions(pad, instruction));
                }
                currentInstructions = nextInstruction;
            }
            complexitySum += currentInstructions.Min(s => s.Length) * int.Parse(code.Remove(code.Length - 1));
        }
        return complexitySum;
    }

    public long P2(string inputFile)
    {
        long complexitySum = 0;
        var codes = GetCodes(inputFile);
        var cache = new Dictionary<(char, char, int), long>();

        foreach (string code in codes)
        {
            char currentPosition = 'A';
            long currentCost = 0;
            foreach (char subTarget in code)
            {
                currentCost += GetMinimalCost(KeypadType.Numpad, currentPosition, subTarget, 25, cache);
                currentPosition = subTarget;
            }

            complexitySum += currentCost * long.Parse(code.Remove(code.Length - 1));
        }
        return complexitySum;
    }

}

class Program
{
    static void Main(string[] args)
    {
        var solution = new Solution();
        string inputFile = "input";
        Console.WriteLine($"Part 1: {solution.P1(inputFile)}");
        Console.WriteLine($"Part 2: {solution.P2(inputFile)}");
    }

}
