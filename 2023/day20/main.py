from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import defaultdict
import math

# High or low pulse

# Flip-flop module (prefix %)
# on or off
# Initially, all flip-flops are off
# If high pulse, ignore.
# If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.

# Conjunction module (prefix &)
# remember type of most recent pulses received from each input
# Initially, all inputs are low pulses
# Starts by updating its memory for the new pulse
# Then, if all inputs are high pulses, it sends a low pulse. Otherwise, it sends a high pulse.

# Broadcast module (named broadcaster)
# Distributes a input pulse to all of its outputs
# Only one of these in the input

# Button module (named button)
# Sends a single low pulse to the broadcast module when pressed

# Never push the button if modules are still processing pulses.

# Breadth first search problem with same order as in input file

@dataclass
class Module:
    name: str
    output_modules: list = field(default_factory=list)

    def get_output_modules(self):
        return self.output_modules
    
    def is_in_output(self, module):
        return module in self.output_modules

    def replace_output_modules(self, output_modules):
        self.output_modules = output_modules

    @abstractmethod
    def process_input(self, input):
        pass

@dataclass
class FlipFlop(Module):
    on: bool = False 

    def process_input(self, input):
        if input.value:
            return None
        self.on = not self.on
        return Input(int(self.on), self)

@dataclass
class Conjunction(Module):
    memory: dict = field(default_factory=dict)

    def process_input(self, input):
        self.memory[input.from_module.name] = input.value
        return Input(0, self) if all(self.memory.values()) else Input(1, self)
    
@dataclass
class Broadcaster(Module):
    def process_input(self, input):
        return Input(input.value, self)

@dataclass
class Input:
    value: int
    from_module: Module

def parse_input(input_path="input.txt"):
    modules = {}
    for line in open(input_path).readlines():
        if line.startswith("%"):
            module_name, raw_output_names = line[1:].split(" -> ")
            output_names = raw_output_names.strip().split(", ")
            flipflop_module = FlipFlop(module_name, output_names)
            modules[module_name] = flipflop_module
        elif line.startswith("&"):
            module_name, raw_output_names = line[1:].split(" -> ")
            output_names = raw_output_names.strip().split(", ")
            conjunction_module = Conjunction(module_name, output_names)
            modules[module_name] = conjunction_module
        else:
            module_name, raw_output_names = line.split(" -> ")
            output_names = raw_output_names.strip().split(", ")
            broadcaster_module = Broadcaster(module_name, output_names)
            modules[module_name] = broadcaster_module
        
    # Update output_modules
    for module in modules.values():
        # Replace output names with module references 
        new_output_modules = []
        for output_name in module.get_output_modules():
            if output_name == 'rx':
                print()
            if output_name in modules:
                new_output_modules.append(modules[output_name])
            else:
                new_output_modules.append(Module(output_name, []))
        module.replace_output_modules(new_output_modules)
    
    # Update Conjunction modules' memory 
    for module in modules.values():
        if isinstance(module, Conjunction):
            for other_module in modules.values():
                if other_module == module: continue
                if not other_module.is_in_output(module): continue
                # Initialize memory to 0
                module.memory[other_module.name] = 0
    return modules

def get_state(modules):
    state = ""
    for module in modules.values():
        if isinstance(module, FlipFlop):
            state += str(int(module.on))
        elif isinstance(module, Conjunction):
            state += "".join(str(val) for val in module.memory.values())
    return state
        

def part_1(modules, target_presses=1000):
    pulse_counter = defaultdict(lambda: defaultdict(int))
    times_pressed = 0
    initial_state = get_state(modules)
    looped = False
    while not looped and times_pressed <= target_presses:
        queue = [(Input(0, None), modules["broadcaster"])]
        times_pressed += 1
        while len(queue) > 0:
            pulse, module = queue.pop(0)
            #print(f"{pulse.from_module.name if pulse.from_module else 'button'} - {pulse.value} -> {module.name}")
            pulse_counter[times_pressed][pulse.value] += 1
            output = module.process_input(pulse)
            if not output: continue
            for output_module in module.get_output_modules():
                queue.append((output, output_module))
        if get_state(modules) == initial_state:
            looped = True
    rest = target_presses % times_pressed
    divider = target_presses // times_pressed
    low_pulses_in_loop = sum(pulse_counter[i][0] for i in range(1, times_pressed+1))
    low_pulses_rest = sum(pulse_counter[i][0] for i in range(1, rest+1))
    high_pulses_in_loop = sum(pulse_counter[i][1] for i in range(1, times_pressed+1))
    high_pulses_rest = sum(pulse_counter[i][1] for i in range(1, rest+1))
    return divider*low_pulses_in_loop*divider*high_pulses_in_loop + low_pulses_rest*high_pulses_rest

# &nc is the only module that points to rx.
# The output of &nc is low pulse if all inputs are high pulses 
# Therefore, to simplify the problem, we can calculate the loops of each input module and take lcm of them to get the total number button presses required 

def part_2(modules):
    pulse_counter = defaultdict(int) 
    input_modules = {}
    for module in modules.values():
        if module.is_in_output(modules["nc"]):
            input_modules[module.name] = None 
    times_pressed = 0
    looped = False
    while not looped:
        queue = [(Input(0, None), modules["broadcaster"])]
        times_pressed += 1
        while len(queue) > 0:
            pulse, module = queue.pop(0)
            if pulse.from_module is not None and pulse.from_module.name in input_modules and pulse.value == 1:
                input_modules[pulse.from_module.name] = times_pressed
            pulse_counter[pulse.value] += 1
            output = module.process_input(pulse)
            if not output: continue
            for output_module in module.get_output_modules():
                queue.append((output, output_module))
        if all(input_modules.values()):
            looped = True
    return math.lcm(*input_modules.values())

def main():
    modules = parse_input()
    print("Part 1: ", part_1(modules))
    modules = parse_input()
    print("Part 2: ", part_2(modules))

if __name__ == "__main__":
    main()