use std::collections::HashSet;
use std::fs;

fn parse_input(input_file: &str) -> Vec<Vec<char>> {
    let raw_data = fs::read_to_string(input_file).expect("Error reading file");
    let mut map_2d: Vec<Vec<char>> = Vec::new();
    for line in raw_data.lines() {
        let mut row: Vec<char> = Vec::new();
        for c in line.chars() {
            row.push(c);
        }
        map_2d.push(row);
    }
    map_2d
}

fn get_starting_position(
    map_2d: &Vec<Vec<char>>,
    num_rows: usize,
    num_cols: usize,
) -> (usize, usize, i32) {
    for i in 0..num_rows {
        for j in 0..num_cols {
            match map_2d[i][j] {
                '>' => return (i, j, 1),
                '<' => return (i, j, 3),
                '^' => return (i, j, 0),
                'v' => return (i, j, 2),
                _ => continue,
            }
        }
    }
    panic!("No starting position found");
}

fn get_obstacles(
    map_2d: &Vec<Vec<char>>,
    num_rows: usize,
    num_cols: usize,
) -> HashSet<(usize, usize)> {
    let mut obstacles = HashSet::new();
    for i in 0..num_rows {
        for j in 0..num_cols {
            if map_2d[i][j] != '#' {
                continue;
            }
            obstacles.insert((i, j));
        }
    }
    obstacles
}

fn p1(
    obstacles: &HashSet<(usize, usize)>,
    num_rows: usize,
    num_cols: usize,
    mut i: usize,
    mut j: usize,
    mut direction: i32,
    threshold: i32,
) -> (usize, bool) {
    let mut visited: HashSet<(usize, usize)> = HashSet::new();
    let mut current_visited_len = visited.len();
    visited.insert((i, j));
    let mut in_map = true;
    let mut not_updates_since = 0;
    while in_map {
        if not_updates_since > threshold {
            return (visited.len(), true);
        }
        if visited.len() == current_visited_len {
            not_updates_since += 1;
        } else {
            current_visited_len = visited.len();
            not_updates_since = 0;
        }
        if direction == 0 {
            // Create a vector of obstacles in the path
            let mut clashing_obstacles = obstacles
                .iter()
                .filter(|&obstacle| obstacle.1 == j && obstacle.0 < i)
                .collect::<Vec<_>>();
            if clashing_obstacles.len() == 0 {
                for k in (0..i).rev() {
                    visited.insert((i, k));
                }
                in_map = false;
            } else {
                clashing_obstacles.sort_by(|a, b| b.0.cmp(&a.0));
                let obstacle = clashing_obstacles[0];
                for k in (obstacle.0 + 1..i).rev() {
                    visited.insert((k, j));
                }
                i = obstacle.0 + 1;
                direction = (direction + 1) % 4;
            }
        } else if direction == 1 {
            let mut clashing_obstacles = obstacles
                .iter()
                .filter(|&obstacle| obstacle.0 == i && obstacle.1 > j)
                .collect::<Vec<_>>();
            if clashing_obstacles.len() == 0 {
                for k in j + 1..num_cols {
                    visited.insert((i, k));
                }
                in_map = false;
            } else {
                clashing_obstacles.sort_by(|a, b| a.1.cmp(&b.1));
                let obstacle = clashing_obstacles[0];
                for k in j + 1..obstacle.1 {
                    visited.insert((i, k));
                }
                j = obstacle.1 - 1;
                direction = (direction + 1) % 4;
            }
        } else if direction == 2 {
            let mut clashing_obstacles = obstacles
                .iter()
                .filter(|&obstacle| obstacle.1 == j && obstacle.0 > i)
                .collect::<Vec<_>>();
            if clashing_obstacles.len() == 0 {
                for k in i + 1..num_rows {
                    visited.insert((k, j));
                }
                in_map = false;
            } else {
                clashing_obstacles.sort_by(|a, b| a.0.cmp(&b.0));
                let obstacle = clashing_obstacles[0];
                for k in i + 1..obstacle.0 {
                    visited.insert((k, j));
                }
                i = obstacle.0 - 1;
                direction = (direction + 1) % 4;
            }
        } else {
            let mut clashing_obstacles = obstacles
                .iter()
                .filter(|&obstacle| obstacle.0 == i && obstacle.1 < j)
                .collect::<Vec<_>>();
            if clashing_obstacles.len() == 0 {
                for k in (0..j).rev() {
                    visited.insert((i, k));
                }
                in_map = false;
            } else {
                clashing_obstacles.sort_by(|a, b| b.1.cmp(&a.1));
                let obstacle = clashing_obstacles[0];
                for k in (obstacle.1 + 1..j).rev() {
                    visited.insert((i, k));
                }
                j = obstacle.1 + 1;
                direction = (direction + 1) % 4;
            }
        }
    }
    (visited.len(), false)
}

fn p2(
    obstacles: &mut HashSet<(usize, usize)>,
    num_rows: usize,
    num_cols: usize,
    start_i: usize,
    start_j: usize,
    direction: i32,
) -> usize {
    let mut num_stuck = 0;
    for i in 0..num_rows {
        for j in 0..num_cols {
            if obstacles.contains(&(i, j)) {
                continue;
            }
            obstacles.insert((i, j));
            let (_, is_stuck) = p1(
                obstacles, num_rows, num_cols, start_i, start_j, direction, 4,
            );
            if is_stuck {
                num_stuck += 1;
            }
            obstacles.remove(&(i, j));
        }
    }
    num_stuck
}

fn main() {
    let input_file = "input.txt";
    let map_2d = parse_input(&input_file);
    let num_rows = map_2d.len();
    let num_cols = map_2d[0].len();
    let (i, j, direction) = get_starting_position(&map_2d, num_rows, num_cols);
    let obstacles = get_obstacles(&map_2d, num_rows, num_cols);
    let (num_visited, _) = p1(&obstacles, num_rows, num_cols, i, j, direction, 4);
    println!("Part 1: {}", num_visited);
    println!(
        "Part 2: {}",
        p2(&mut obstacles.clone(), num_rows, num_cols, i, j, direction)
    )
}
