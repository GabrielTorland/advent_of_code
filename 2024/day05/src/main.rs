use std::collections::HashMap;
use std::fs;

fn parse(file_name: &str) -> (HashMap<i32, Vec<i32>>, Vec<Vec<i32>>) {
    let raw_data = fs::read_to_string(file_name).expect("Error reading file");
    // split on double new line
    let groups: Vec<&str> = raw_data.split("\n\n").collect();

    let mut rules: HashMap<i32, Vec<i32>> = HashMap::new();
    for line in groups[0].lines() {
        let (before, after) = line.split_once("|").unwrap();
        let key = before.trim().parse::<i32>().unwrap();
        let value: i32 = after.trim().parse::<i32>().unwrap();
        if !rules.contains_key(&key) {
            rules.insert(key, Vec::new());
        }
        if !rules.contains_key(&value) {
            rules.insert(value, Vec::new());
        }

        let targets = rules.get_mut(&key).unwrap();
        targets.push(value);
    }

    let mut updates: Vec<Vec<i32>> = Vec::new();

    for line in groups[1].lines() {
        let elements: Vec<i32> = line
            .split(",")
            .map(|x| x.trim().parse::<i32>().unwrap())
            .collect();
        updates.push(elements);
    }

    (rules, updates)
}

fn p1(rules: &HashMap<i32, Vec<i32>>, updates: &Vec<Vec<i32>>) -> i32 {
    let mut valid_updates: Vec<usize> = Vec::new();
    'update_loop: for (i, update) in updates.iter().enumerate() {
        for (j, value) in update.iter().enumerate() {
            let before = &update[..j];
            let after = rules.get(value).unwrap();
            if after.iter().any(|x| before.contains(x)) {
                continue 'update_loop;
            }
        }
        valid_updates.push(i);
    }
    let mut middle_values: Vec<i32> = Vec::new();
    for i in valid_updates.iter() {
        let current_update = &updates[*i];
        let middle_index = (current_update.len() - 1) / 2;
        middle_values.push(current_update[middle_index]);
    }
    middle_values.iter().sum()
}

fn p2(rules: &HashMap<i32, Vec<i32>>, updates: &Vec<Vec<i32>>) -> i32 {
    let mut new_updates: Vec<Vec<i32>> = Vec::new();
    for update in updates {
        // Only consider the incorrect updates
        let mut is_correct = true;
        for (j, value) in update.iter().enumerate() {
            let before = &update[..j];
            let after = rules.get(value).unwrap();
            if after.iter().any(|x| before.contains(x)) {
                is_correct = false;
                break;
            }
        }
        if is_correct {
            continue;
        }

        let mut in_degree: HashMap<i32, i32> = HashMap::new();

        for page_number in rules.keys() {
            if !update.contains(page_number) {
                continue;
            }
            in_degree.insert(*page_number, 0);
        }

        // Find the number of incoming edges for each page number
        for (page_number, targets) in rules.iter() {
            if !update.contains(page_number) {
                continue;
            }
            for target in targets {
                // Only consider the page numbers in the update
                if !update.contains(target) {
                    continue;
                }
                let count = in_degree.get_mut(target).unwrap();
                *count += 1;
            }
        }

        let mut queue: Vec<i32> = Vec::new();

        // Initialize the queue with the independent page numbers
        for (page_number, count) in in_degree.iter() {
            if *count == 0 {
                queue.push(*page_number);
            }
        }

        let mut result: Vec<i32> = Vec::new();

        // Topological sort
        while !queue.is_empty() {
            let current = queue.pop().unwrap();
            result.push(current);

            let targets = rules.get(&current).unwrap();
            for target in targets {
                if !update.contains(target) {
                    continue;
                }
                let count = in_degree.get_mut(target).unwrap();
                *count -= 1;
                if count == &0 {
                    queue.push(*target);
                }
            }
        }

        new_updates.push(result);
    }

    let mut middle_values: Vec<i32> = Vec::new();
    for current_update in new_updates.iter() {
        let middle_index = (current_update.len() - 1) / 2;
        middle_values.push(current_update[middle_index]);
    }
    middle_values.iter().sum()
}

fn main() {
    let file_name = "input.txt";
    let (rules, updates) = parse(file_name);
    println!("Part 1: {}", p1(&rules, &updates));
    println!("Part 2: {}", p2(&rules, &updates));
}
