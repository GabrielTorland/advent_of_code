namespace Day08;

using System.IO;
using System;
using System.Numerics;
using System.Collections;
using System.Collections.Immutable;

using Map = System.Collections.Immutable.ImmutableDictionary<System.Numerics.Complex, char>;


class Solution
{

    public int Part1(string inputFile) => GetUniquePositions(inputFile, GetAntinodes1).Count();
    public int Part2(string inputFile) => GetUniquePositions(inputFile, GetAntinodes2).Count();
    Map GetMap(string inputFile)
    {
        string[] lines = File.ReadAllLines(inputFile);

        return (
            from y in Enumerable.Range(0, lines.Length)
            from x in Enumerable.Range(0, lines[0].Length)
            select new KeyValuePair<Complex, char>(x - y * Complex.ImaginaryOne, lines[y][x])
        ).ToImmutableDictionary();
    }

    HashSet<Complex> GetUniquePositions(string inputFile, GetAntinodes getAntinodes)
    {
        Map map = GetMap(inputFile);

        // get antenna locations
        var antennas = (
            from pos in map.Keys
            where char.IsAsciiLetterOrDigit(map[pos])
            select pos
        ).ToArray();

        return (
            from srcAntenna in antennas
            from dstAntenna in antennas
            where srcAntenna != dstAntenna && map[srcAntenna] == map[dstAntenna]
            from antinode in getAntinodes(srcAntenna, dstAntenna, map)
            select antinode
        ).ToHashSet();
    }

    // Allow passing the antinodes functions as arguments
    delegate IEnumerable<Complex> GetAntinodes(Complex srcAntenna, Complex dstAntenna, Map map);

    IEnumerable<Complex> GetAntinodes1(Complex srcAntenna, Complex dstAntenna, Map map)
    {
        var dir = dstAntenna - srcAntenna;
        var antinode = dstAntenna + dir;
        if (map.Keys.Contains(antinode))
        {
            yield return antinode;
        }
    }
    IEnumerable<Complex> GetAntinodes2(Complex srcAntenna, Complex dstAntenna, Map map)
    {
        var dir = dstAntenna - srcAntenna;
        var antinode = dstAntenna;
        while (map.Keys.Contains(antinode))
        {
            yield return antinode;
            antinode += dir;
        }
    }

}

class Program
{
    static void Main(string[] args)
    {
        Solution solution = new Solution();
        Console.WriteLine($"Part 1: {solution.Part1("input.txt")}");
        Console.WriteLine($"Part 2: {solution.Part2("input.txt")}");
    }
}
