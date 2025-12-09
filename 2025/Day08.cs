using System.Text.RegularExpressions;

namespace AdventOfCode;

public class Day08 : BaseDay
{
    private readonly List<(int, int, int)> _points = [];

    public double GetDistance((int, int, int) p1, (int, int, int) p2)
    {
        return Math.Pow(p1.Item1 - p2.Item1, 2) + Math.Pow(p1.Item2 - p2.Item2, 2) + Math.Pow(p1.Item3 - p2.Item3, 2);
    }

    public ValueTask<string> P1()
    {
        var distancesAndPoints = new HashSet<(double, int, int)>();
        for (int i = 0; i < _points.Count; i++)
        {
            for (int j = i + 1; j < _points.Count; j++)
            {
                var p1 = _points[i];
                var p2 = _points[j];

                var distance = GetDistance(p1, p2);

                distancesAndPoints.Add((distance, i, j));
            }
        }


        var circuits = new List<HashSet<int>>();
        foreach (var (distance, i, j) in distancesAndPoints.OrderBy(x => x.Item1).Take(1000))
        {
            HashSet<int> candidate1 = default;
            HashSet<int> candidate2 = default;
            foreach (var circuit in circuits)
            {
                if (circuit.Contains(i) || circuit.Contains(j))
                {
                    if (candidate1 == default)
                    {
                        candidate1 = circuit;
                    }
                    else
                    {
                        candidate2 = circuit;
                    }
                }
            }

            if (candidate1 != default && candidate2 != default)
            {
                foreach (var x in candidate2)
                {
                    candidate1.Add(x);
                }

                circuits.Remove(candidate2);
                candidate1.Add(i);
                candidate1.Add(j);
            }
            else if (candidate1 == default && candidate2 == default)
            {
                circuits.Add(new HashSet<int>{ i, j });
            }
            else
            {
                candidate1.Add(i);
                candidate1.Add(j);
            }
        }

        var result = 1L;
        foreach (var circuit in circuits.OrderByDescending(circuit => circuit.Count).Take(3))
        {
            result *= circuit.Count;
        }

         return ValueTask.FromResult(result.ToString());
    }


    public ValueTask<string> P2()
    {
        var circuits = new List<HashSet<int>>();
        var distancesAndPoints = new HashSet<(double, int, int)>();
        for (int i = 0; i < _points.Count; i++)
        {
            for (int j = i + 1; j < _points.Count; j++)
            {
                var p1 = _points[i];
                var p2 = _points[j];

                var distance = GetDistance(p1, p2);

                distancesAndPoints.Add((distance, i, j));
            }
            circuits.Add(new HashSet<int>{ i });
        }

        foreach (var (distance, i, j) in distancesAndPoints.OrderBy(x => x.Item1))
        {
            HashSet<int> candidate1 = default;
            HashSet<int> candidate2 = default;
            foreach (var circuit in circuits)
            {
                if (circuit.Contains(i) || circuit.Contains(j))
                {
                    if (candidate1 == default)
                    {
                        candidate1 = circuit;
                    }
                    else
                    {
                        candidate2 = circuit;
                    }
                }
            }

            if (candidate1 != default && candidate2 != default)
            {
                foreach (var x in candidate2)
                {
                    candidate1.Add(x);
                }
                circuits.Remove(candidate2);

                candidate1.Add(i);
                candidate1.Add(j);
                if (circuits.Count == 1 && candidate1.Count == 1000){
                    return ValueTask.FromResult(((long)_points[i].Item1*(long)_points[j].Item1).ToString());
                }

            }
            else if (candidate1 == default && candidate2 == default)
            {
                circuits.Add(new HashSet<int>{ i, j });
            }
            else
            {
                candidate1.Add(i);
                candidate1.Add(j);
                if (circuits.Count == 1 && candidate1.Count == 1000){
                    return ValueTask.FromResult(((long)_points[i].Item1*(long)_points[j].Item1).ToString());
                }
            }
        }

        return ValueTask.FromResult("No solution.");
    }

    public Day08()
    {
        foreach (var pointRaw in File.ReadLines("Inputs/08.txt"))
        {
            var point = pointRaw.Split(',');
            var x = int.Parse(point[0]);
            var y = int.Parse(point[1]);
            var z = int.Parse(point[2]);

            _points.Add((x, y, z));
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
