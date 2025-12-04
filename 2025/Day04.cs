using System;

namespace AdventOfCode;

public class Day04 : BaseDay
{
    private readonly char[,] _map;
    private int _rows;
    private int _cols;

    public ValueTask<string> P1()
    {
        var deltas = new List<(int, int)>{ (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1) };
        var accessible = 0;
        for (int i = 0; i < _rows; i++)
        {
            for (int j = 0; j < _cols; j++)
            {
                if (_map[i, j] == '@')
                {
                    var neighbours = 0;
                    foreach (var (di, dj) in deltas)
                    {
                        var iNeighbour = i + di;
                        var jNeighbour = j + dj;

                        if (iNeighbour < 0 || iNeighbour >= _rows || jNeighbour < 0 || jNeighbour >= _cols)
                        {
                            continue;
                        }

                        if (_map[iNeighbour, jNeighbour] == '@')
                        {
                            neighbours++;
                        }
                    }

                    if (neighbours < 4)
                    {
                        accessible++;
                    }
                }
            }
        }

        return ValueTask.FromResult(accessible.ToString());
    }


    public ValueTask<string> P2()
    {
        var deltas = new List<(int, int)>{ (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1) };
        var accessible = 0;
        var currentlyAccessible = new Stack<(int, int)>();
        do {

            while (currentlyAccessible.Count() > 0)
            {
                var (i, j) = currentlyAccessible.Pop();
                _map[i, j] = '.';
            }

            for (int i = 0; i < _rows; i++)
            {
                for (int j = 0; j < _cols; j++)
                {
                    if (_map[i, j] == '@')
                    {
                        var neighbours = 0;
                        foreach (var (di, dj) in deltas)
                        {
                            var iNeighbour = i + di;
                            var jNeighbour = j + dj;

                            if (iNeighbour < 0 || iNeighbour >= _rows || jNeighbour < 0 || jNeighbour >= _cols)
                            {
                                continue;
                            }

                            if (_map[iNeighbour, jNeighbour] == '@')
                            {
                                neighbours++;
                            }
                        }

                        if (neighbours < 4)
                        {
                            accessible++;
                            currentlyAccessible.Push((i, j));
                        }
                    }
                }
            }
        } while (currentlyAccessible.Count() > 0);

        return ValueTask.FromResult(accessible.ToString());
    }

    public Day04()
    {
        var inputPath = "Inputs/04.txt";
        var lines = File.ReadAllLines(inputPath);
        _rows = lines.Length;
        _cols = lines.First().Length;

        _map = new char[_rows, _cols];

        for (int i = 0; i < _rows; i++)
        {
            for (int j = 0; j < _cols; j++)
            {
                _map[i, j] = lines[i][j];
            }
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
