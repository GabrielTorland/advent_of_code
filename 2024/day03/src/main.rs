use regex::Regex;
use std::fs;

fn parse_input(input_file: &str) -> String {
    fs::read_to_string(input_file).expect("Something went wrong reading the file")
}

fn p1(input: &str) -> i32 {
    let mut result = 0;
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    for mat in re.captures_iter(input) {
        let x = mat.get(1).unwrap().as_str().parse::<i32>().unwrap();
        let y = mat.get(2).unwrap().as_str().parse::<i32>().unwrap();
        result += x * y;
    }
    result
}

fn p2(input: &str) -> i32 {
    let mut result = 0;
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)").unwrap();
    let mut skip = false;
    for mat in re.captures_iter(input) {
        let match_str = mat.get(0).unwrap().as_str();
        if match_str == "do()" {
            skip = false;
        } else if match_str == "don't()" {
            skip = true;
        } else if !skip {
            let x = mat.get(1).unwrap().as_str().parse::<i32>().unwrap();
            let y = mat.get(2).unwrap().as_str().parse::<i32>().unwrap();
            result += x * y;
        }
    }
    result
}

fn main() {
    let input_file = "input.txt";
    let input = parse_input(input_file);
    println!("Part 1: {}", p1(&input));
    println!("Part 2: {}", p2(&input));
}
