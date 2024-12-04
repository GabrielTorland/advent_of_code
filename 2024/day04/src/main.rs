use std::fs;

fn parse_input(input_file: &str) -> Vec<Vec<char>> {
    let contents = fs::read_to_string(input_file).expect("Something went wrong reading the file");
    let mut grid: Vec<Vec<char>> = Vec::new();
    for line in contents.lines() {
        let mut row: Vec<char> = Vec::new();
        for c in line.chars() {
            row.push(c);
        }
        grid.push(row);
    }
    grid
}

fn p1(grid: &Vec<Vec<char>>) -> i32 {
    let mut target = ['X', 'M', 'A', 'S'];
    let mut occurrences = 0;
    let mut grid_found = grid.clone();
    for i in 0..grid.len() {
        for j in 0..grid[i].len() {
            grid_found[i][j] = '.';
        }
    }
    for i in 0..grid.len() {
        for j in 0..grid[i].len() {
            if !['X', 'S'].contains(&grid[i][j]) {
                continue;
            }

            if grid[i][j] == 'X' && target[0] != 'X' || grid[i][j] == 'S' && target[0] != 'S' {
                target.reverse();
            }

            // check down
            if (i + target.len()) <= grid.len() {
                'down: {
                    for delta in 0..target.len() {
                        if grid[i + delta][j] != target[delta] {
                            break 'down;
                        }
                    }
                    occurrences += 1;
                    for delta in 0..target.len() {
                        grid_found[i + delta][j] = target[delta];
                    }
                }
            }

            // check up
            if (target.len() - 1) <= i {
                'up: {
                    for delta in 0..target.len() {
                        if grid[i - delta][j] != target[delta] {
                            break 'up;
                        }
                    }
                    occurrences += 1;
                    for delta in 0..target.len() {
                        grid_found[i - delta][j] = target[delta];
                    }
                }
            }

            // check right
            if (j + target.len()) <= grid[i].len() {
                'right: {
                    for delta in 0..target.len() {
                        if grid[i][j + delta] != target[delta] {
                            break 'right;
                        }
                    }
                    occurrences += 1;
                    for delta in 0..target.len() {
                        grid_found[i][j + delta] = target[delta];
                    }
                }
            }

            // check left
            if (target.len() - 1) <= j {
                'left: {
                    for delta in 0..target.len() {
                        if grid[i][j - delta] != target[delta] {
                            break 'left;
                        }
                    }
                    occurrences += 1;
                    for delta in 0..target.len() {
                        grid_found[i][j - delta] = target[delta];
                    }
                }
            }

            // check diagonal up left
            if (target.len() - 1) <= i && (target.len() - 1) <= j {
                'up_left: {
                    for delta in 0..target.len() {
                        if grid[i - delta][j - delta] != target[delta] {
                            break 'up_left;
                        }
                    }
                    occurrences += 1;
                    for delta in 0..target.len() {
                        grid_found[i - delta][j - delta] = target[delta];
                    }
                }
            }

            // check diagonal up right
            if (target.len() - 1) <= i && (j + target.len()) <= grid[i].len() {
                'up_right: {
                    for delta in 0..target.len() {
                        if grid[i - delta][j + delta] != target[delta] {
                            break 'up_right;
                        }
                    }
                    occurrences += 1;
                    for delta in 0..target.len() {
                        grid_found[i - delta][j + delta] = target[delta];
                    }
                }
            }

            // check diagonal down left
            if (i + target.len()) <= grid.len() && (target.len() - 1) <= j {
                'down_left: {
                    for delta in 0..target.len() {
                        if grid[i + delta][j - delta] != target[delta] {
                            break 'down_left;
                        }
                    }
                    occurrences += 1;
                    for delta in 0..target.len() {
                        grid_found[i + delta][j - delta] = target[delta];
                    }
                }
            }

            // check diagonal down right
            if (i + target.len()) <= grid.len() && (j + target.len()) <= grid[i].len() {
                'down_right: {
                    for delta in 0..target.len() {
                        if grid[i + delta][j + delta] != target[delta] {
                            break 'down_right;
                        }
                    }
                    occurrences += 1;
                    for delta in 0..target.len() {
                        grid_found[i + delta][j + delta] = target[delta];
                    }
                }
            }
        }
    }
    // print gird_found
    for i in 0..grid_found.len() {
        for j in 0..grid_found[i].len() {
            print!("{}", grid_found[i][j]);
        }
        println!();
    }
    occurrences / 2
}

fn p2(grid: &Vec<Vec<char>>) -> i32 {
    let mut occurrences = 0;
    for i in 0..grid.len() {
        for j in 0..grid[i].len() {
            if grid[i][j] != 'A' {
                continue;
            }

            if i == 0 || (i + 1) == grid.len() || j == 0 || (j + 1) == grid[i].len() {
                continue;
            }

            if ((grid[i - 1][j + 1] == 'M' && grid[i + 1][j - 1] == 'S')
                || (grid[i - 1][j + 1] == 'S' && grid[i + 1][j - 1] == 'M'))
                && ((grid[i - 1][j - 1] == 'M' && grid[i + 1][j + 1] == 'S')
                    || (grid[i - 1][j - 1] == 'S' && grid[i + 1][j + 1] == 'M'))
            {
                occurrences += 1;
            }
        }
    }
    occurrences
}

fn main() {
    let input_file = "input.txt";
    let grid = parse_input(input_file);
    println!("Part 1: {}", p1(&grid));
    println!("Part 2: {}", p2(&grid));
}
