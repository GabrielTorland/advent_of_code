using ScottPlot;

namespace AdventOfCode;

public class Day09 : BaseDay
{
    private readonly List<(int, int)> _redTiles = [];
    private readonly HashSet<(int, int)> _greenTiles = [];

    private long GetArea((int, int) tile1, (int, int) tile2)
    {
        var width = Math.Abs(tile1.Item1 - tile2.Item1) + 1;
        var height = Math.Abs(tile1.Item2 - tile2.Item2) + 1;

        var area = (long)width*(long)height;

        return area;
    }

    private long GetAreaOfRectangle((int, int, int, int) rectangle)
    {
        var height = rectangle.Item2 - rectangle.Item1 + 1;
        var width = rectangle.Item4 - rectangle.Item3 + 1;

        var area = (long)width*(long)height;

        return area;
    }

    public ValueTask<string> P1()
    {
        var maxArea = 0L;
        for (int i = 0; i < _redTiles.Count; i++)
        {
            var tile1 = _redTiles[i];
            for (int j = i + 1; j < _redTiles.Count; j++)
            {
                var tile2 = _redTiles[j];
                var area = GetArea(tile1, tile2);

                if (area > maxArea)
                {
                    maxArea = area;
                }
            }

        }

        return ValueTask.FromResult(maxArea.ToString());
    }

    private void AddGreenTiles()
    {
        foreach (var group in _redTiles.GroupBy(tile => tile.Item1))
        {
            var i = 0;
            var tiles = group.OrderBy(tile => tile.Item2).ToArray();
            while (i < group.Count() - 1)
            {
                var currentTile = tiles[i];
                var nextTile = tiles[i+1];
                for (int x = currentTile.Item2 + 1; x < nextTile.Item2; x++)
                {
                    _greenTiles.Add((currentTile.Item1, x));
                }

                i++;
            }
        }

        foreach (var group in _redTiles.GroupBy(tile => tile.Item2))
        {
            var i = 0;
            var tiles = group.OrderBy(tile => tile.Item1).ToArray();
            while (i < group.Count() - 1)
            {
                var currentTile = tiles[i];
                var nextTile = tiles[i+1];
                for (int y = currentTile.Item1 + 1; y < nextTile.Item1; y++)
                {
                    _greenTiles.Add((y, currentTile.Item2));
                }

                i++;
            }
        }
    }

    private Dictionary<int, (int, int)> GetHorizontalVertices()
    {
        var tiles = new List<(int, int)>();
        tiles.AddRange(_greenTiles);
        tiles.AddRange(_redTiles);

        var orderedHorizontalVertices = new Dictionary<int, (int, int)>();
        foreach (var group in tiles.GroupBy(tile => tile.Item1))
        {
            var orderedTiles = group.OrderBy(tile => tile.Item2);

            var startTile = orderedTiles.First();
            var endTile = orderedTiles.Last();

            orderedHorizontalVertices.Add(startTile.Item1, (startTile.Item2, endTile.Item2));
        }

        return orderedHorizontalVertices;
    }


    private void PlotTiles(List<(int, int, int)> vertices, string plotName = "tiles_plot.png", (int, int, int, int)? rectangle = null)
    {
        var points = new List<(int, int)>();
        points.AddRange(_redTiles);
        points.AddRange(_greenTiles);

        var pointCount = points.Count();
        double[] xs = new double[pointCount];
        double[] ys = new double[pointCount];

        Random rand = new Random(0);
        for (int i = 0; i < pointCount; i++)
        {
            xs[i] = points[i].Item2;
            ys[i] = points[i].Item1;
        }

        ScottPlot.Plot myPlot = new();

        myPlot.Add.ScatterPoints(xs, ys);

        if (vertices.Count > 0)
        {
            foreach(var vertex in vertices)
            {
                var y = vertex.Item1;
                var x0 = vertex.Item2;
                var x1 = vertex.Item3;
                myPlot.Add.Line(x0, y, x1, y);
            }
        }

        if (rectangle.HasValue)
        {
            var rect = myPlot.Add.Rectangle(rectangle.Value.Item3, rectangle.Value.Item4, rectangle.Value.Item2, rectangle.Value.Item1);
        }

        myPlot.Title("Tiles");
        myPlot.XLabel("X Axis");
        myPlot.YLabel("Y Axis");

        myPlot.SavePng($"/mnt/c/Users/gabri/Downloads/{plotName}", 800, 800);
    }

    public ValueTask<string> P2()
    {
        AddGreenTiles();
        //PlotTiles();

        var rectangles = new List<(int, int, int, int)>();
        for (int i = 0; i < _redTiles.Count; i++)
        {
            for (int j = i + 1; j < _redTiles.Count; j++)
            {
                int[] xs = [_redTiles[i].Item2, _redTiles[j].Item2];
                int[] ys = [_redTiles[i].Item1, _redTiles[j].Item1];
                rectangles.Add((ys.Min(), ys.Max(), xs.Min(), xs.Max()));
            }
        }

        var horizontalVertices = GetHorizontalVertices();

        var vertices = new List<(int, int, int)>();
        foreach (var item in horizontalVertices)
        {
            vertices.Add((item.Key, item.Value.Item1, item.Value.Item2));
        }

        foreach (var rectangle in rectangles.OrderByDescending(GetAreaOfRectangle))
        {
            var y0 = rectangle.Item1;
            var y1 = rectangle.Item2;
            var x0 = rectangle.Item3;
            var x1 = rectangle.Item4;

            var isValid = true;
            for (var i = y0; i < y1+1; i++)
            {
                var vertex = horizontalVertices[i];

                if (vertex.Item1 > x0 || vertex.Item2 < x1)
                {
                    isValid = false;
                    break;
                }
            }

            if (isValid)
            {
                return ValueTask.FromResult(GetAreaOfRectangle(rectangle).ToString());
            }
        }

        return ValueTask.FromResult("hi mom");
    }

    public Day09()
    {
        foreach (var pointRaw in File.ReadLines("Inputs/09.txt"))
        {
            var greenTile = pointRaw.Split(',');
            var x = int.Parse(greenTile[0]);
            var y = int.Parse(greenTile[1]);
            _redTiles.Add((y, x));
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
