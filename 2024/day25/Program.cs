


class Solution
{
    (List<int[]>, List<int[]>) GetKeysAndLocks(string fileName)
    {
        var keys = new List<int[]>();
        var locks = new List<int[]>();
        foreach (var raw in File.ReadAllText(fileName).Split("\n\n"))
        {
            var lines = raw.Trim().Split('\n');

            var keyLock = Enumerable.Range(0, lines[0].Length)
                .Select(x => Enumerable.Range(0, lines.Length)
                        .Count(y => lines[y][x] == '#')).ToArray();

            if (lines[0][0] == '#')
            {
                locks.Add(keyLock);

            }
            else
            {
                keys.Add(keyLock);
            }
        }
        return (keys, locks);
    }

    List<int[]> GetCorrectKeys(int[] doorLock, List<int[]> keys)
    {
        var possibleKeys = new List<int[]>(keys);

        for (int i = 0; i < doorLock.Length; i++)
        {
            possibleKeys = possibleKeys.Where(k => (k[i] + doorLock[i] <= 7)).ToList();
        }
        return possibleKeys;
    }

    public int P1(string fileName)
    {
        (var keys, var locks) = GetKeysAndLocks(fileName);

        int result = 0;
        foreach (var doorLock in locks)
        {
            var correctKeys = GetCorrectKeys(doorLock, keys);
            result += correctKeys.Count();
        }

        return result;
    }

}

class Program
{

    static void Main(string[] args)
    {
        string fileName = "input";
        var solution = new Solution();
        System.Console.WriteLine($"Part 1: {solution.P1(fileName)}");
    }
}
