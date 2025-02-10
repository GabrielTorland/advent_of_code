
class MemoryBlock:
    def __init__(self, file_ids, used, free):
        self.file_ids = file_ids
        self.used = used
        self.free = free
        self.start_offset = 0

class FileSystem:
    def __init__(self):
        self.disk = []
        self.leftmost_free_block_idx = 0
        self.num_files = 0

    def add_memory_block(self, memory_block):
        self.disk.append(memory_block)

    def optimize_disk_fragmentation(self):
        while self.leftmost_free_block_idx < (len(self.disk)-1):
            last_block = self.disk[-1]
            # Move files from last block to leftmost free block
            if self.disk[self.leftmost_free_block_idx].free > last_block.used:
                self.disk[self.leftmost_free_block_idx].free -= last_block.used
                self.disk[self.leftmost_free_block_idx].file_ids.extend(last_block.file_ids)
                self.disk.pop()
            # Move parts of the files from last block to leftmost free block
            else:
                files_2_move = []
                move_size = self.disk[self.leftmost_free_block_idx].free
                files_2_move.append((last_block.file_ids[0][0], move_size))
                last_block.file_ids[0] = (last_block.file_ids[0][0], last_block.file_ids[0][1] - move_size)
                last_block.used -= move_size
                last_block.free += move_size
                self.disk[self.leftmost_free_block_idx].free = 0
                self.disk[self.leftmost_free_block_idx].used += move_size
                self.disk[self.leftmost_free_block_idx].file_ids.extend(files_2_move)
                for i in range(self.leftmost_free_block_idx+1, len(self.disk)):
                    if self.disk[i].free > 0:
                        self.leftmost_free_block_idx = i
                        break

    def optimize_disk_files(self):
        current_block_idx = len(self.disk)-1
        while current_block_idx > 0:
            current_block = self.disk[current_block_idx]
            if len(current_block.file_ids) > 1:
                for i in range(self.leftmost_free_block_idx, current_block_idx):
                    if self.disk[i].free >= current_block.file_ids[0][1]:
                        self.disk[i].free -= current_block.file_ids[0][1]
                        self.disk[i].used += current_block.file_ids[0][1]
                        self.disk[i].file_ids.append(current_block.file_ids[0])
                        current_block.used -= current_block.file_ids[0][1]
                        current_block.free += current_block.file_ids[0][1]
                        current_block.start_offset += current_block.file_ids[0][1]
                        current_block.file_ids.pop(0)
                        break
            else:
                for i in range(self.leftmost_free_block_idx, current_block_idx):
                    if self.disk[i].free >= current_block.used:
                        self.disk[i].free -= current_block.used
                        self.disk[i].used += current_block.used
                        self.disk[i].file_ids.extend(current_block.file_ids)
                        current_block.file_ids = []
                        current_block.free = current_block.used + current_block.free
                        current_block.used = 0
                        break
            current_block_idx -= 1

    def get_hash(self):
        fs_hash = 0
        idx = 0
        for memory_block in self.disk:
            if memory_block.free != 0:
                idx += memory_block.start_offset
            for file_id, size in memory_block.file_ids:
                for _ in range(size):
                    fs_hash += file_id*idx
                    idx += 1
            idx += max(memory_block.free-memory_block.start_offset, 0)
        return fs_hash

def parse(input_file="input.txt"):
    raw_data = open(input_file, "r").read().strip()
    fs = FileSystem()
    for i in range(0, len(raw_data)-1, 2):
        memory_block = MemoryBlock([(fs.num_files,int(raw_data[i]))], int(raw_data[i]), int(raw_data[i+1]))
        fs.add_memory_block(memory_block)
        fs.num_files += 1
    memory_block = MemoryBlock([(fs.num_files,int(raw_data[-1]))], int(raw_data[-1]), 0)
    fs.add_memory_block(memory_block)
    fs.num_files += 1
    return fs

if __name__ == "__main__":
    fs = parse()
    fs.optimize_disk_fragmentation()
    print("Part 1:", fs.get_hash())
    fs = parse()
    fs.optimize_disk_files()
    print("Part 2:", fs.get_hash())
