use std::fs;

fn parse_input(contents: &str) -> (Vec<i32>, Vec<i32>) {
    let mut loc1_ids: Vec<i32> = Vec::new();
    let mut loc2_ids: Vec<i32> = Vec::new();

    for line in contents.lines() {
        let mut values = line.split_whitespace();

        let loc1_id = values.next().map(|id| id.parse::<i32>().unwrap()).unwrap();
        let loc2_id = values.next().map(|id| id.parse::<i32>().unwrap()).unwrap();

        loc1_ids.push(loc1_id);
        loc2_ids.push(loc2_id);
    }

    (loc1_ids, loc2_ids)
}

fn p1(loc1_ids: &Vec<i32>, loc2_ids: &Vec<i32>) -> i32 {
    let mut diffs: Vec<i32> = Vec::new();

    debug_assert_eq!(
        loc1_ids.len(),
        loc2_ids.len(),
        "Location lengths must match"
    );

    for (loc1, loc2) in loc1_ids.iter().zip(loc2_ids.iter()) {
        let diff = (loc1 - loc2).abs();
        diffs.push(diff);
    }

    diffs.iter().sum()
}

fn p2(loc1_ids: &Vec<i32>, loc2_ids: &Vec<i32>) -> i32 {
    let mut similarity_score_numbers = Vec::new();
    for loc1_id in loc1_ids.iter() {
        let count: i32 = loc2_ids
            .iter()
            .filter(|&id| id == loc1_id)
            .count()
            .try_into()
            .unwrap();
        similarity_score_numbers.push(loc1_id * count);
    }
    similarity_score_numbers.iter().sum()
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Failed to read input.txt");
    let (mut loc1_ids, mut loc2_ids) = parse_input(&contents);

    loc1_ids.sort();
    loc2_ids.sort();
    let result_p1 = p1(&loc1_ids, &loc2_ids);
    println!("Part 1: {}", result_p1);

    let result_p2 = p2(&loc1_ids, &loc2_ids);
    println!("Part 2: {}", result_p2);
}
