using ScottPlot;

namespace AdventOfCode;

public class Day10 : BaseDay
{
    private readonly List<IndicatorLight> _indicatorLights = [];

    public static int BoolsToShort(IEnumerable<bool> bools)
    {

        var boolsArray = bools.ToArray();

        int result = 0;
        for (int i = 0; i < boolsArray.Length; i++)
        {
            if (boolsArray[i])
            {
                result = (int)(result | (1 << i));
            }
        }

        return result;
    }

    public class Button(int stateUpdater)
    {
        private int _stateUpdater = stateUpdater;

        public (int, int[]) ClickButton(int currentState, int[] currentJoltageCount)
        {

            var newJoltageCount = (int[])currentJoltageCount.Clone();
            for (int i = 0; i < currentJoltageCount.Length; i++)
            {
                newJoltageCount[i] += _stateUpdater & (int)Math.Pow(2, i);
            }

            return (currentState ^ _stateUpdater, newJoltageCount);
        }
    }

    public class IndicatorLight(int targetState, int[] targetJoltageCount, int currentState, int[] currentJoltageCount, int numberOfLights, int currentButtonPresses, Button[] buttons)
    {
        private int _targetState = targetState;

        private int[] _targetJoltageCount = targetJoltageCount;

        public int CurrentState { get; set; } = currentState;

        public int[] CurrentJoltageCount = currentJoltageCount;

        public int NumberOfLights { get; set; } = numberOfLights;

        public int CurrentButtonPresses = currentButtonPresses;

        public Button[] Buttons { get; set; } = buttons;


        public bool StateMatchesTarget()
        {
            return CurrentState == _targetState;
        }

        public bool StateMatchesTargetV2()
        {
            if (!StateMatchesTarget())
            {
                return false;
            }

            for (int i = 0; i < _targetJoltageCount.Length; i++)
            {
                if (CurrentJoltageCount[i] != _targetJoltageCount[i])
                {
                    return false;
                }
            }

            return true;

        }

        public bool isValidJoltageCount()
        {
            for (int i = 0; i < _targetJoltageCount.Length; i++)
            {
                if (CurrentJoltageCount[i] > _targetJoltageCount[i])
                {
                    return false;
                }
            }

            return true;
        }

        public IndicatorLight GetChild(int newState, int[] newJoltageCount)
        {
            return new IndicatorLight(_targetState, _targetJoltageCount, newState, CurrentJoltageCount, NumberOfLights, CurrentButtonPresses, Buttons);
        }
    }

    public ValueTask<string> P1()
    {
        var result = 0;
        foreach (var indicatorLight in _indicatorLights)
        {
            var priorityQueue = new PriorityQueue<IndicatorLight, int>();
            priorityQueue.Enqueue(indicatorLight, indicatorLight.CurrentButtonPresses);
            while (true)
            {
                var anIndicatorLight = priorityQueue.Dequeue();

                if (anIndicatorLight.StateMatchesTarget())
                {
                    result += anIndicatorLight.CurrentButtonPresses;
                    break;
                }

                foreach (var button in anIndicatorLight.Buttons)
                {
                    var (newState, newJoltageCount) = button.ClickButton(anIndicatorLight.CurrentState, anIndicatorLight.CurrentJoltageCount);
                    var child = anIndicatorLight.GetChild(newState, newJoltageCount);
                    child.CurrentButtonPresses++;
                    priorityQueue.Enqueue(child, child.CurrentButtonPresses);
                }
            }
        }

        return ValueTask.FromResult(result.ToString());
    }

    public ValueTask<string> P2()
    {
        return ValueTask.FromResult("Solved in python:/");
    }

    public Day10()
    {

        foreach (var line in File.ReadLines("Inputs/10test.txt"))
        {
            var segments = line.Split(' ').ToArray();
            var target = segments.First().Trim(['[', ']']).Select(c => c == '#').ToArray();
            var numberOfLights = target.Length;
            var targetState = BoolsToShort(target);

            var buttons = new List<Button>();
            for (int i = 1; i < segments.Count() - 1; i++)
            {
                int stateUpdater = 0;
                var lightIndices = segments[i].Trim(['(', ')']).Split(',').Select(int.Parse).ToArray();
                foreach (var lightIndex in lightIndices)
                {
                    stateUpdater += (int)Math.Pow(2, lightIndex);
                }

                buttons.Add(new Button(stateUpdater));
            }

            var targetJoltageCount = segments.Last().Trim(['{', '}']).Split(',').Select(int.Parse).ToArray();

            int initialState = 0;
            int[] initialJoltageCount = new int[targetJoltageCount.Count()];
            _indicatorLights.Add(new IndicatorLight(targetState, targetJoltageCount, initialState, initialJoltageCount, numberOfLights, 0, buttons.ToArray()));
        }
    }

    public override ValueTask<string> Solve_1() => P1();

    public override ValueTask<string> Solve_2() => P2();
}
