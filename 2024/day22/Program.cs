


class Solution
{
    IEnumerable<long> GetInitialSecretNumbers(string inputFile)
    {
        foreach (var line in File.ReadAllLines(inputFile))
        {
            yield return long.Parse(line.Trim());
        }

    }

    long PredictFutureSecretNumber(long secretNumber, int steps)
    {
        var currentNumber = secretNumber;
        for (int step = 0; step < steps; step++)
        {
            currentNumber = ((currentNumber * 64) ^ currentNumber) % 16777216;
            currentNumber = ((currentNumber / 32) ^ currentNumber) % 16777216;
            currentNumber = ((currentNumber * 2048) ^ currentNumber) % 16777216;
        }
        return currentNumber;
    }


    void CalculateProfits(long initialSecretNumber, Dictionary<string, int> profits)
    {
        var prices = new List<int>();
        var changes = new List<int>();
        var currentNumber = initialSecretNumber;
        var visited = new HashSet<string>();

        for (int i = 0; i < 2000; i++)
        {
            currentNumber = PredictFutureSecretNumber(currentNumber, 1);
            var currentPrice = currentNumber.ToString().Last() - '0';
            if (i > 0)
            {
                changes.Add(currentPrice - prices.Last());
            }
            prices.Add(currentPrice);

            if (changes.Count >= 4)
            {
                var seq = String.Concat(changes.Skip(changes.Count - 4));
                if (visited.Contains(seq))
                {
                    continue;
                }
                profits[seq] = profits.GetValueOrDefault(seq) + currentPrice;
                visited.Add(seq);
            }
        }
    }

    public long P1(string inputFile)
    {
        long sum = 0;
        foreach (var initialSecretNumber in GetInitialSecretNumbers(inputFile))
        {
            sum += PredictFutureSecretNumber(initialSecretNumber, 2000);
        }

        return sum;
    }

    public int P2(string inputFile)
    {
        var initialScretNumbers = GetInitialSecretNumbers(inputFile).ToList();

        var profits = new Dictionary<string, int>();

        foreach (var secretNumber in initialScretNumbers)
        {
            CalculateProfits(secretNumber, profits);
        }

        return profits.Values.Max();

    }

}


class Program
{
    static void Main(string[] args)
    {
        string inputFile = "input";
        var solution = new Solution();
        System.Console.WriteLine($"Part 1: {solution.P1(inputFile)}");
        System.Console.WriteLine($"Part 2: {solution.P2(inputFile)}");
    }
}
