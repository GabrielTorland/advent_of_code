
class Solution
{

    private Dictionary<long, long> GetStones(string inputFile)
    {

        long[] rawStones = File.ReadAllText(inputFile).Split(' ').Select(long.Parse).ToArray();

        var stones = new Dictionary<long, long>();

        foreach (long stone in rawStones)
        {
            if (!stones.ContainsKey(stone))
            {
                stones[stone] = 1;
            }
            else
            {
                stones[stone]++;
            }
        }

        return stones;
    }

    private Dictionary<long, long> RunSimulation(Dictionary<long, long> stones, long steps)
    {
        for (long step = 0; step < steps; step++)
        {
            var nextStones = new Dictionary<long, long>();
            foreach (KeyValuePair<long, long> stone in stones)
            {

                if (stone.Key == 0)
                {
                    AddOrUpdate(nextStones, 1, stone.Value);
                }
                else if (stone.Key.ToString().Count() % 2 == 0)
                {
                    string stoneStr = stone.Key.ToString();

                    long nextStone = long.Parse(stoneStr.Substring(0, stoneStr.Count() / 2));
                    AddOrUpdate(nextStones, nextStone, stone.Value);

                    nextStone = long.Parse(stoneStr.Substring(stoneStr.Count() / 2));
                    AddOrUpdate(nextStones, nextStone, stone.Value);
                }
                else
                {
                    AddOrUpdate(nextStones, stone.Key * 2024, stone.Value);
                }

            }
            stones = nextStones;
            Console.WriteLine($"Number of stones: {stones.Count()}");
        }
        return stones;
    }

    private void AddOrUpdate(Dictionary<long, long> dict, long key, long value)
    {
        if (dict.ContainsKey(key))
        {
            dict[key] += value;
        }
        else
        {
            dict[key] = value;
        }
    }

    public long P1()
    {
        var stones = GetStones("input");
        stones = RunSimulation(stones, 25);
        return stones.Sum(item => item.Value);
    }
    public long P2()
    {
        var stones = GetStones("input");
        stones = RunSimulation(stones, 75);
        return stones.Sum(item => item.Value);
    }

}

class Program()
{

    static void Main(string[] args)
    {
        var solution = new Solution();
        Console.WriteLine($"Part 1: {solution.P1()}");
        Console.WriteLine($"Part 2: {solution.P2()}");
    }

}

