using System.Numerics;

namespace AoC.Y2024.Day9;



class FileSystem
{
    private List<(int? FileID, int Size)> _memory;

    private int _firstEmptySegmentIndex;


    public FileSystem(string rawFilesystem)
    {
        _memory = new List<(int?, int)>();
        for (int i = 0; i < rawFilesystem.Length; i += 1)
        {
            if (i % 2 == 1)
            {
                // Add empty space
                _memory.Add((null, rawFilesystem[i] - '0'));
            }
            else
            {
                int fileID = i / 2;
                // Add file
                _memory.Add((fileID, rawFilesystem[i] - '0'));
            }

        }
        _firstEmptySegmentIndex = 1;

    }

    public (int? FileID, int Size) GetSegment(int index)
    {
        if (index < 0 || index >= _memory.Count)
        {
            throw new IndexOutOfRangeException($"Index {index} is out of range for memory with size {_memory.Count}");
        }
        return _memory[index];
    }

    public void SetSegment(int index, (int? FileID, int Size) segment)
    {
        if (index < 0 || index >= _memory.Count)
        {
            throw new IndexOutOfRangeException($"Index {index} is out of range for memory with size {_memory.Count}");
        }
        _memory[index] = segment;
    }

    public void RemoveSegment(int index)
    {
        if (index < 0 || index >= _memory.Count)
        {
            throw new IndexOutOfRangeException($"Index {index} is out of range for memory with size {_memory.Count}");
        }
        _memory.RemoveAt(index);

    }

    public void InsertSegment(int index, (int? FileID, int Size) segment)
    {
        if (index < 0 || index > _memory.Count)
        {
            throw new IndexOutOfRangeException($"Index {index} is out of range for insertion into memory with size {_memory.Count}");
        }
        _memory.Insert(index, segment);
    }

    public void OptimizeFilesystemV1()
    {
        int i = _memory.Count - 1;

        while (_firstEmptySegmentIndex <= i)
        {

            var currentSegment = GetSegment(i);

            if (currentSegment.FileID == null)
            {
                RemoveSegment(i);
                i--;
            }
            else
            {
                var emptySegment = GetSegment(_firstEmptySegmentIndex);

                if (emptySegment.Size < currentSegment.Size)
                {
                    SetSegment(_firstEmptySegmentIndex, (currentSegment.FileID, emptySegment.Size));
                    _firstEmptySegmentIndex += 2;
                    SetSegment(i, (currentSegment.FileID, currentSegment.Size - emptySegment.Size));
                }
                else if (emptySegment.Size > currentSegment.Size)
                {
                    RemoveSegment(i);
                    InsertSegment(_firstEmptySegmentIndex, currentSegment);
                    _firstEmptySegmentIndex++;
                    SetSegment(_firstEmptySegmentIndex, (null, emptySegment.Size - currentSegment.Size));

                }
                else
                {
                    RemoveSegment(i);
                    i--;
                    SetSegment(_firstEmptySegmentIndex, currentSegment);
                    _firstEmptySegmentIndex += 2;
                }
            }
        }

        if (_memory[i].FileID == null)
        {
            RemoveSegment(i);
        }

    }

    public void OptimizeFilesystemV2()
    {
        int i = _memory.Count - 1;

        while (i > 1)
        {

            var currentSegment = GetSegment(i);

            if (currentSegment.FileID == null)
            {
                RemoveSegment(i);
                i--;
            }
            else
            {
                for (int j = 0; j < i; j++)
                {
                    var emptySegment = GetSegment(j);
                    if (emptySegment.FileID != null)
                    {
                        continue;
                    }
                    if (emptySegment.Size > currentSegment.Size)
                    {
                        RemoveSegment(i);
                        InsertSegment(j, currentSegment);
                        SetSegment(j + 1, (null, emptySegment.Size - currentSegment.Size));
                        break;
                    }
                    else if (emptySegment.Size == currentSegment.Size)
                    {
                        RemoveSegment(i);
                        SetSegment(j, currentSegment);
                        i++;
                        break;
                    }
                }
                i--;
            }
        }

        if (_memory[i].FileID == null)
        {
            RemoveSegment(i);
        }

    }

    public BigInteger GetHash()
    {
        BigInteger sum = 0;
        int index = 0;
        for (int i = 0; i < _memory.Count; i++)
        {
            (int? FileID, int Size) segment = _memory[i];

            int count = segment.Size;
            while (count != 0)
            {
                if (segment.FileID == null)
                {
                    sum += index * 0;
                }
                else
                {
                    sum += index * segment.FileID.Value;
                }
                index += 1;
                count -= 1;
            }
        }
        return sum;
    }

}

class Solution
{
    public BigInteger Part1(string inputFile)
    {
        string rawFilesystem = File.ReadAllText(inputFile);
        var fs = new FileSystem(rawFilesystem);
        fs.OptimizeFilesystemV1();
        return fs.GetHash();
    }

    public BigInteger Part2(string inputFile)
    {
        string rawFilesystem = File.ReadAllText(inputFile);
        var fs = new FileSystem(rawFilesystem);
        fs.OptimizeFilesystemV2();
        return fs.GetHash();
    }

}

class Program
{
    static void Main(string[] args)
    {
        string inputFile = "test.txt";
        var solution = new Solution();
        Console.WriteLine($"Part 1: {solution.Part1(inputFile)}");
        Console.WriteLine($"Part 2: {solution.Part2(inputFile)}");

    }
}