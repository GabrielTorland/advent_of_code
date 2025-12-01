using System;

namespace AdventOfCode;

public class Day01 : BaseDay
{
    private readonly string[] _operations;

    public ValueTask<string> P1()
    {
        var zeros = 0;
        var currentPosition = 50;

        foreach (var operation in _operations)
        {
            var direction = operation[0];
            var clicks = int.Parse(operation.Substring(1));

            if (direction == 'R')
            {
                currentPosition += clicks;
            }
            else
            {
                currentPosition -= clicks;
            }

            currentPosition = currentPosition % 100;

            if (currentPosition == 0)
            {
                zeros++;
            }
        }

        return ValueTask.FromResult(zeros.ToString());
    }

    public ValueTask<string> P2()
    {
        var zeros = 0;
        var currentPosition = 50;
        var nextPoistion = currentPosition;
        foreach (var operation in _operations)
        {

            var direction = operation[0];
            var clicks = int.Parse(operation.Substring(1));

            if (direction == 'R')
            {
                nextPoistion += clicks;
            }
            else
            {
                nextPoistion -= clicks;
            }


            var dividend = clicks/100;
            if (dividend > 0)
            {
                zeros += dividend;
            }


            var reminder = clicks % 100;
            if (currentPosition != 0 && (direction == 'L' && currentPosition - reminder <= 0) || (direction == 'R' && currentPosition + reminder >= 100))
            {
                zeros++;
            }

            currentPosition = nextPoistion % 100;
            if (currentPosition < 0)
            {
                currentPosition += 100;
            }

            nextPoistion = currentPosition;
        }
        return ValueTask.FromResult(zeros.ToString());
    }

    public Day01()
    {
        var data = File.ReadAllText(InputFilePath);
        var operations = data.Split("\n").ToList();
        operations.RemoveAt(operations.Count-1);
        _operations = operations.ToArray();
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
