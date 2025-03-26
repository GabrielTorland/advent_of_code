namespace AoC.Y2024.D017;

using System.Text.RegularExpressions;


class Solution
{

    public string P1()
    {
	(var registers, var program) = GetRegistersAndProgram("input");
	// add a timer to see how ulong it takes
	return String.Join(", ",
		from num in RunProgramFast(program, (ulong)registers['A'])
		select num.ToString()
	       );
    }

    public ulong P2()
    {
	(var registers, var program) = GetRegistersAndProgram("input");
	return FindA(program, 0, 0);

    }

    (Dictionary<char, int>, int[]) GetRegistersAndProgram(string inputFile)
    {

	string rawInput = File.ReadAllText(inputFile);
	var registers = new Dictionary<char, int>();

	string pattern = @"Register (\w): (\d+)";

	foreach (Match registerMatch in Regex.Matches(rawInput, pattern))
	{
	    registers[registerMatch.Groups[1].Value.ToCharArray()[0]] = int.Parse(registerMatch.Groups[2].Value);
	}

	pattern = @"Program: ([\d,]+)";

	Match programMatch = Regex.Match(rawInput, pattern);

	int[] program = programMatch.Groups[1].Value.Split(',').Select(int.Parse).ToArray();

	return (registers, program);
    }

    int GetOperandValue(int operand, Dictionary<char, int> registers)
    {
	switch (operand)
	{
	    case int n when n >= 0 && n <= 3:
		return operand;
	    case 4:
		return registers['A'];
	    case 5:
		return registers['B'];
	    case 6:
		return registers['C'];
	    default:
		throw new Exception("Invalid operand");
	}
    }

    // Ineffective method used for part 1
    string RunProgram(int[] program, Dictionary<char, int> registers)
    {
	int instructionPointer = 0;

	List<int> output = new List<int>();

	int iterations = 0;

	while (instructionPointer < program.Length)
	{
	    int opcode = program[instructionPointer];
	    int literalOperand = program[instructionPointer + 1];
	    int operandValue = GetOperandValue(literalOperand, registers);

	    switch (opcode)
	    {
		case 0: // adv instruction
		    registers['A'] = registers['A'] >> operandValue;
		    instructionPointer += 2;
		    break;
		case 1: // bxl instruction
		    registers['B'] = registers['B'] ^ literalOperand;
		    instructionPointer += 2;
		    break;
		case 2: // bst
		    registers['B'] = operandValue % 8;
		    instructionPointer += 2;
		    break;
		case 3: // jnz
		    if (registers['A'] == 0)
		    {
			instructionPointer += 2;
		    }
		    else
		    {
			instructionPointer = literalOperand;
		    }
		    break;
		case 4: // bxc
		    registers['B'] = registers['B'] ^ registers['C'];
		    instructionPointer += 2;
		    break;
		case 5: // out
		    output.Add(operandValue % 8);
		    instructionPointer += 2;
		    iterations++;
		    break;
		case 6: // bdv
		    registers['B'] = registers['A'] >> operandValue;
		    instructionPointer += 2;
		    break;
		case 7: // cdv
		    registers['C'] = registers['A'] >> operandValue;
		    instructionPointer += 2;
		    break;
		default:
		    throw new Exception("Invalid opcode");
	    }
	}
	Console.WriteLine(iterations);
	return String.Join(", ", output.Select(num => num.ToString()));
    }

    int[] RunProgramFast(int[] program, ulong a)
    {
	List<int> output = new List<int>();

	ulong b = 0;
	ulong c = 0;

	int iterations = 0;

	while (a != 0 || iterations == 0)
	{
	    b = (a % 8) ^ 5;
	    c = (a >> (int)b);
	    b = (b ^ 6) ^ c;
	    output.Add((int)(b % 8));
	    a = (a >> 3);
	    iterations++;
	}

	return output.ToArray();
    }

    bool isSegmentEqual(int[] program, int[] outputSegment, int startIndex, int count)
    {
	for (int i = startIndex; i < startIndex + count; i++)
	{
	    if (program[i] != outputSegment[i - startIndex])
	    {
		return false;
	    }
	}
	return true;
    }

    ulong FindA(int[] program, ulong a, int i)
    {
	int programSize = program.Length;

	Queue<(ulong, int)> queue = new Queue<(ulong, int)>();
	queue.Enqueue((a, i));

	while (queue.Count() > 0)
	{
	    (a, i) = queue.Dequeue();
	    if (i == programSize)
	    {
		int[] result = RunProgramFast(program, a >> 3);
		Console.WriteLine(String.Join(", ", result.Select(num => num.ToString())));
		return a >> 3;
	    }
	    for (ulong currentA = a; currentA < a + 8; currentA++)
	    {
		if (isSegmentEqual(program, RunProgramFast(program, currentA), programSize - i - 1, i + 1))
		{
		    queue.Enqueue((currentA << 3, i + 1));
		}
	    }
	}
	return 0;

    }

}

class Program
{


    static void Main(string[] args)
    {
	var solution = new Solution();
	Console.WriteLine($"Part 1: {solution.P1()}");
	Console.WriteLine($"Part 2: {solution.P2()}");
    }
}
