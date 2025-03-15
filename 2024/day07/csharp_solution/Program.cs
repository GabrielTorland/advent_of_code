

using System.Numerics;
using System.Reflection.Emit;

namespace Day7
{

    class InputParser
    {
        public static List<Equation> Parse(string inputFile)
        {
            List<Equation> equations = new List<Equation>();

            foreach (string line in File.ReadAllLines(inputFile))
            {
                string[] rawNumbers = line.Replace(":", "").Split(' ');
                var equation = new Equation(BigInteger.Parse(rawNumbers[0]), rawNumbers.Skip(1).Select(BigInteger.Parse).ToArray());
                equations.Add(equation);

            }
            return equations;
        }
    }


    class Equation
    {
        public BigInteger Target { get; }
        public BigInteger[] Operands { get; }

        public Equation(BigInteger target, BigInteger[] operands)
        {
            Target = target;
            Operands = operands;
        }

        public bool IsSolvable(BigInteger currentValue, int index, Func<BigInteger, BigInteger, BigInteger>[] operators)
        {
            if (index + 1 == Operands.Length)
            {
                return currentValue == Target;
            }

            foreach (var op in operators)
            {
                BigInteger newValue = op(currentValue, Operands[index + 1]);
                if (IsSolvable(newValue, index + 1, operators))
                {
                    return true;
                }
            }

            return false;
        }
    }

    class P1
    {
        public static BigInteger Solve(List<Equation> equations)
        {
            BigInteger result = 0;
            foreach (Equation equation in equations)
            {
                Func<BigInteger, BigInteger, BigInteger>[] operators = new Func<BigInteger, BigInteger, BigInteger>[]
                {
                    (a, b) => a + b,           // Addition
                    (a, b) => a * b,           // Multiplication
                };

                if (equation.IsSolvable(0, -1, operators))
                {
                    result += equation.Target;
                }
            }
            return result;
        }
    }

    class P2
    {
        public static BigInteger Solve(List<Equation> equations)
        {
            BigInteger result = 0;
            foreach (Equation equation in equations)
            {
                Func<BigInteger, BigInteger, BigInteger>[] operators = new Func<BigInteger, BigInteger, BigInteger>[]
                {
                    (a, b) => a + b,           // Addition
                    (a, b) => a * b,           // Multiplication
                    (a, b) => BigInteger.Parse(a.ToString() + b.ToString())
                };

                if (equation.IsSolvable(0, -1, operators))
                {
                    result += equation.Target;
                }
            }
            return result;
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            List<Equation> equations = InputParser.Parse("input.txt");
            BigInteger resultP1 = P1.Solve(equations);
            Console.WriteLine($"Part 1: {resultP1}");
            BigInteger resultP2 = P2.Solve(equations);
            Console.WriteLine($"Part 2: {resultP2}");
        }
    }

}