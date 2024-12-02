use std::fs;

fn parse(input_file: &str) -> Vec<Vec<i32>> {
    let input = fs::read_to_string(input_file).expect("Unable to read file");
    let mut result = Vec::new();
    for line in input.lines() {
        let mut row = Vec::new();
        for num in line.split_whitespace() {
            row.push(num.parse::<i32>().unwrap());
        }
        result.push(row);
    }
    result
}

fn is_safe_report(report: &Vec<i32>) -> (bool, Option<usize>) {
    let mut increasing: bool = true;
    let mut decreasing: bool = true;

    for i in 0..(report.len() - 1) {
        let diff = report[i] - report[i + 1];

        if diff.abs() < 1 || diff.abs() > 3 {
            return (false, Some(i));
        }
        if diff > 0 {
            increasing = false;
        } else if diff < 0 {
            decreasing = false;
        }
        // Check if the report is not consistently increasing or decreasing
        if !increasing && !decreasing {
            return (false, Some(i));
        }
    }
    (true, None)
}

fn p1(reports: &Vec<Vec<i32>>) -> i32 {
    let mut num_safe_reports = 0;
    for report in reports {
        let (safe_report, _) = is_safe_report(&report);
        if !safe_report {
            continue;
        }
        num_safe_reports += 1;
    }
    num_safe_reports
}

fn p2(reports: &Vec<Vec<i32>>) -> i32 {
    let mut num_safe_reports = 0;
    for report in reports {
        let (safe_report, i) = is_safe_report(&report);
        if !safe_report {
            let mut copy_report = report.clone();
            let index = i.unwrap();

            // Edge case: the first pair is in the opposite direction as the rest
            if index == 1 {
                copy_report.remove(index - 1);
                let (safe_report, _) = is_safe_report(&copy_report);
                if safe_report {
                    num_safe_reports += 1;
                    continue;
                }
            }

            copy_report = report.clone();
            copy_report.remove(index);
            let (safe_report, _) = is_safe_report(&copy_report);
            if safe_report {
                num_safe_reports += 1;
                continue;
            }
            copy_report = report.clone();
            copy_report.remove(index + 1);
            let (safe_report, _) = is_safe_report(&copy_report);
            if safe_report {
                num_safe_reports += 1;
                continue;
            }
        } else {
            num_safe_reports += 1;
        }
    }
    num_safe_reports
}

fn main() {
    let input_file = "input.txt";
    let reports = parse(input_file);
    println!("Part 1: {}", p1(&reports));
    println!("Part 2: {}", p2(&reports));
}
