#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <regex>
#include <filesystem>
#include <stack>
#include <bits/stdc++.h>

#define INF 99999

class Valve {
public:
    std::string id;
    int index;
    int rate;
    std::vector<Valve*> neighbors;
    Valve(std::string id, int index, int rate) {
        this->id = id;
        this->index = index;
        this->rate = rate;
    }
    void add_neighbor(Valve* neighbor){
        this->neighbors.push_back(neighbor);
    }
};

class Worker{
public:
    int released_pressure;
    int time;
    Valve* valve;
    Worker(int released_pressure, int time, Valve* valve){
        this->released_pressure = released_pressure;
        this->time = time;
        this->valve = valve;
    }
    std::vector<Valve*>& neighbors(){
        return this->valve->neighbors;
    }
};

class TwoWorkers{
public:
    Worker* worker1;
    Worker* worker2;
    std::unordered_set<std::string>* activated;
    TwoWorkers(Worker* worker1, Worker* worker2, std::unordered_set<std::string>* activated){
        this->worker1 = worker1;
        this->worker2 = worker2;
        this->activated = activated;
    }
    ~TwoWorkers(){
        delete this->activated;
        delete this->worker1;
        delete this->worker2;
    }
    int released_pressure(){
        return this->worker1->released_pressure + this->worker2->released_pressure;
    }
    int worker_1_time(){
        return this->worker1->time;
    }
    std::vector<Valve*> worker_1_neighbors(){
        return this->worker1->neighbors();
    }
    int worker_1_released_pressure(){
        return this->worker1->released_pressure;
    }
    Valve* worker_1_valve(){
        return this->worker1->valve;
    }

    int worker_2_time(){
        return this->worker2->time;
    }
    std::vector<Valve*> worker_2_neighbors(){
        return this->worker2->neighbors();
    }
    int worker_2_released_pressure(){
        return this->worker2->released_pressure;
    }
    Valve* worker_2_valve(){
        return this->worker2->valve;
    }

};

std::map<std::string, Valve*> parse(std::string filename) {
    // the working directory was set to the cmake-build-debug folder
    // just changed working directory to the parent folder
    // this might not be the best solution, but it works
    std::filesystem::current_path(std::filesystem::current_path().parent_path());
    std::ifstream file;
    file.open(filename, std::ios::in);

    // Check if the file was successfully opened
    if (!file) {
        throw std::runtime_error("Unable to open file");
    }

    auto valves = std::map<std::string, Valve*>();
    auto neighbors = std::map<std::string, std::vector<std::string>>();

    // Create a regular expression to match the pattern
    std::regex pattern(R"(([A-Z]{2}).*rate=(\d+).*valves? (.*))");

    // Read the contents of the file line by line
    std::string line;
    int i = 0;
    while (std::getline(file, line)) {
        // Use std::regex_search to find the pattern in the current line
        std::smatch match;
        if (std::regex_search(line, match, pattern)) {
            // storing match in Valve object
            valves[match[1]] = new Valve(match[1], i, std::stoi(match[2]));
            // storing neighbors in a map
            neighbors[match[1]] = std::vector<std::string>();

            std::string raw = match[3];
            std::string delimiter = ", ";
            size_t pos;
            while ((pos = raw.find(delimiter)) != std::string::npos) {
                neighbors[match[1]].push_back(raw.substr(0, pos));
                raw.erase(0, pos + delimiter.length());
            }
            neighbors[match[1]].push_back(raw.substr(0, 2));
            i++;
        }

    }
    // Close the file
    file.close();

    // iterate over the neighbors map and with key and value
    // change the neighbors parameter in the Valve object
    for (auto const& [key, value] : neighbors) {
        // iterate over the vector of neighbors
        for (auto const& neighbor : value) {
            // get the valve object from the valves map
            auto valve = valves[neighbor];
            if (valve == nullptr) {
                throw std::runtime_error("Valve not found");
            }
            valves[key]->add_neighbor(valve);
        }
    }
    return valves;
}


int** floyd_warshall(Valve* valves[], int n)
{

    int i, j, k;

    // create a 2D array of size n*n
    auto D = new int*[n];
    for (i = 0; i < n; i++) {
        D[i] = new int[n];
        for (j = 0; j < n; j++) {
            if (i == j) {
                D[i][j] = 0;
            }
            // check if the index of one of the neighbors of valves[i] is equal to j
            else if (std::find_if(valves[i]->neighbors.begin(), valves[i]->neighbors.end(), [j](Valve* v) { return v->index == j; }) != valves[i]->neighbors.end()) {
                D[i][j] = 1;
            }
            else {
                D[i][j] = INF;
            }
        }
    }

    for (k = 0; k < n; k++) {
        for (i = 0; i < n; i++) {
            for (j = 0; j < n; j++) {
                if (D[i][j] > (D[i][k] + D[k][j]) && D[i][k] != INF && D[k][j] != INF)
                    D[i][j] = D[i][k] + D[k][j];
            }
        }
    }
    return D;
}

bool is_pressure_promising(Valve* valves[], const int n, TwoWorkers* current, const int max_pressure){
    int potential_pressure = current->released_pressure();
    int time_1 = current->worker_1_time();
    int time_2 = current->worker_2_time();
    std::vector<Valve*> valves_left;
    for (int i = 0; i < n; ++i){
        if (current->activated->find(valves[i]->id) == current->activated->end()){
            valves_left.push_back(valves[i]);
        }
    }
    std::sort(valves_left.begin(), valves_left.end(), [](Valve *a, Valve *b) {
        return a->rate > b->rate;
    });
    for (auto const& valve : valves_left) {
        if (time_1 > time_2){
            time_1 -= 2;
            if (time_1 <= 0){
                continue;
            }
            potential_pressure += valve->rate * time_1;
        } else {
            time_2 -= 2;
            if (time_2 <= 0){
                continue;
            }
            potential_pressure += valve->rate * time_2;
        }
    }
    return potential_pressure > max_pressure;
}

void gen_next_steps_one_worker(std::stack<TwoWorkers*>* stack, Valve* valves[], Worker* worker,
                                   Worker* other, std::unordered_set<std::string>* activated, int** D, const int n) {
    int i;
    for (i = 0; i < n; ++i) {
        if (worker->valve->index != i && activated->find(valves[i]->id) == activated->end()
            && valves[i]->rate != 0 && (worker->time - D[worker->valve->index][i] - 1) > 0) {
            auto new_activated = new std::unordered_set<std::string>(*activated);
            new_activated->insert(valves[i]->id);
            auto worker1 = new Worker(worker->released_pressure +
                                      valves[i]->rate * (worker->time - D[worker->valve->index][i] - 1),
                                      worker->time - D[worker->valve->index][i] - 1, valves[i]);
            auto worker2 = new Worker(other->released_pressure, other->time, other->valve);
            stack->push(new TwoWorkers(worker1, worker2, new_activated));
        }
    }
}
void gen_next_steps_two_workers(std::stack<TwoWorkers*>* stack, Valve* valves[], TwoWorkers* current, int** D, const int n){
    int i, j;
    for (i = 0; i < n; ++i){
        if (current->worker1->valve->index != i && current->activated->find(valves[i]->id) == current->activated->end()
        && valves[i]->rate != 0 && (current->worker_1_time() - D[current->worker_1_valve()->index][i] - 1) > 0){
            auto new_activated = new std::unordered_set<std::string>(*current->activated);
            new_activated->insert(valves[i]->id);
            for (j = 0; j < n; ++j){
                if (current->worker2->valve->index != j && new_activated->find(valves[j]->id) == new_activated->end()
                && valves[j]->rate != 0 && (current->worker_2_time() - D[current->worker_2_valve()->index][j] - 1) > 0){
                    auto new_new_activated = new std::unordered_set<std::string>(*new_activated);
                    new_new_activated->insert(valves[j]->id);
                    auto worker1 = new Worker(current->worker_1_released_pressure() +
                                              valves[i]->rate*(current->worker_1_time() - D[current->worker_1_valve()->index][i] - 1),
                                              current->worker_1_time() - D[current->worker_1_valve()->index][i] - 1, valves[i]);
                    auto worker2 = new Worker(current->worker_2_released_pressure() +
                            valves[j]->rate*(current->worker_2_time() - D[current->worker_2_valve()->index][j] - 1),
                            current->worker_2_time() - D[current->worker_2_valve()->index][j] - 1, valves[j]);
                    stack->push(new TwoWorkers(worker1, worker2, new_new_activated));
                }
            }
            delete new_activated;
        }
    }
}

bool done(Valve* valves[], const int n, Worker* worker, std::unordered_set<std::string>* activated, int** D){
    for (int i = 0; i < n; ++i){
        if (worker->valve->index != i && activated->find(valves[i]->id) == activated->end()
            && valves[i]->rate != 0 && (worker->time - D[worker->valve->index][i] - 1) > 0){
            return false;
        }
    }
    return true;
}

int maximize_pressure(Valve* valves[], int** D, const int n, const int t1, const int t2, const int start){
    int max_pressure = 0;
    auto activated = new std::unordered_set<std::string>();
    auto worker_1 = new Worker(0, t1, valves[start]);
    auto worker_2 = new Worker(0, t2, valves[start]);
    auto workers = new TwoWorkers(worker_1, worker_2, activated);
    auto stack = std::stack<TwoWorkers*>();
    stack.push(workers);
    while (!stack.empty()){
        auto current = stack.top();
        stack.pop();
        if (!is_pressure_promising(valves, n, current, max_pressure)){
            delete current;
            continue;
        }
        auto w1_done = done(valves, n, current->worker1, current->activated, D);
        auto w2_done = done(valves, n, current->worker2, current->activated, D);
        if (w1_done && w2_done){
            max_pressure = std::max(max_pressure, current->released_pressure());
        }
        else if (w1_done){
            gen_next_steps_one_worker(&stack, valves, current->worker2, current->worker1, current->activated, D, n);
        }
        else if (w2_done){
            gen_next_steps_one_worker(&stack, valves, current->worker1, current->worker2, current->activated, D, n);
        }
        else{
            gen_next_steps_two_workers(&stack, valves, current, D, n);
        }
        delete current;
    }
    return max_pressure;
}



int main() {
    auto map_valves = parse( "input.txt");
    int n = (int)map_valves.size();
    // store the valves in an array
    Valve* array_valves[map_valves.size()];
    int i = 0;
    for (auto const& [key, value] : map_valves) {
        array_valves[i] = value;
        i++;
    }
    // sort the array of valves by index in a non-decreasing order. The size of the array is n.
    std::sort(array_valves, array_valves + n, [](Valve* a, Valve* b) { return a->index < b->index; });

    // the 2D array D contains all the shortest paths from each vertex to every other vertex
    auto D = floyd_warshall(array_valves, n);
    std::cout << "Part 1: " << maximize_pressure(array_valves, D, n, 30, 0, map_valves["AA"]->index) << std::endl;
    std::cout << "Part 2: " << maximize_pressure(array_valves, D, n, 26, 26, map_valves["AA"]->index) << std::endl;
    return 0;
}