#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>

class Node{
public:
    int number;
    Node* next;
    Node* prev;
};

class EncryptedFile{
public:
    Node* current;
    std::vector<Node*>* original_order;
    int n;
    int rem;
    int numb;
    int moves = 0;

   EncryptedFile(std::vector<Node*>* nodes, int numb){
        this->current = *nodes->begin();
        auto start = nodes->begin();
        auto end = nodes->end();
        (*start)->prev = *(end-1);
        (*start)->next = *(start+1);
        (*(end-1))->prev = *(end-2);
        (*(end-1))->next = *(start);
        for (auto it = start+1; it+1 != end; ++it){
            (*it)->next = *(it+1);
            (*it)->prev = *(it-1);
        }
        this->original_order = nodes;
        this->n = nodes->size();
        this->rem = numb % (this->n-1);
        this->numb = numb;
   }
   ~EncryptedFile(){
       for (auto it = this->original_order->begin(); it != this->original_order->end(); ++it){
           delete *it;
       }
       delete this->original_order;
   }
   void move(){
       auto current_node = this->current;
       auto rng = ((std::abs(current_node->number) % (this->n-1))*this->rem) % (this->n-1);
       if (current_node->number < 0 && rng != 0){
           current_node->prev->next = current_node->next;
           current_node->next->prev = current_node->prev;
           auto iter = current_node;
           for (int i = 0; i < rng; ++i){
               iter = iter->prev;
           }
           auto prev = iter->prev;
           iter->prev->next = current_node;
           iter->prev = current_node;
           current_node->next = iter;
           current_node->prev = prev;
       }
       else if (current_node->number > 0 && rng != 0){
           current_node->prev->next = current_node->next;
           current_node->next->prev = current_node->prev;
           auto iter = current_node;
           for (int i = 0; i < rng; ++i){
               iter = iter->next;
           }
           auto next = iter->next;
           iter->next->prev = current_node;
           iter->next = current_node;
           current_node->prev = iter;
           current_node->next = next;
       }
       this->moves++;
       this->current = *(this->original_order->begin() + (this->moves % this->n));
   }
   long int sum_design_nums_after_zero(){
       long int sum = 0;
       auto tmp = this->current;
       while (tmp->number != 0){
           tmp = tmp->next;
       }
       for (int i = 0; i < 3000; ++i){
           tmp = tmp->next;
           if ((i + 1) % 1000 == 0){
               sum += (long int)tmp->number*(long int)(this->numb);
           }
       }
       return sum;
   }
};

EncryptedFile* parse(std::string filename, int _const){
    std::ifstream file;
    file.open(filename, std::ios::in);

    // Check if the file was successfully opened
    if (!file) {
        throw std::runtime_error("Unable to open file");
    }

    auto nodes = new std::vector<Node*>();

    // Read the file line by line
    std::string line;
    while (std::getline(file, line)) {
        // Convert the line to an integer
        std::stringstream ss(line);
        int numb;
        ss >> numb;
        nodes->push_back(new Node{numb, nullptr, nullptr});
    }

    auto encrypted_file = new EncryptedFile(nodes, _const);
    return encrypted_file;
}

long int simulate(EncryptedFile* encrypted_file, const int moves){
    for (int i = 0; i < moves; ++i){
        encrypted_file->move();
    }
    return encrypted_file->sum_design_nums_after_zero();
}

int main() {
    auto encrypted_file = parse("./input.txt", 1);
    std::cout << "Part 1: " << simulate(encrypted_file, encrypted_file->n) << std::endl; // 6387
    delete encrypted_file;
    auto encrypted_file_2 = parse("./input.txt", 811589153);
    std::cout << "Part 2: " << simulate(encrypted_file_2,10*encrypted_file_2->n) << std::endl; // 2455057187825
    delete encrypted_file_2;
    return 0;
}
