class Directory():
    def __init__(self, name, upper=None):
        self.name = name
        self.upper = upper
        self.files = {}
        self.subdirs = {}

    def add_file(self, size, name):
        self.files[name] = size

    def add_dir(self, name):
        self.subdirs[name] = Directory(name, self)

    def size(self):
        size = sum(self.files.values())
        for subdir in self.subdirs.values():
            size += subdir.size()
        return size

    def all_sizes(self):
        list_sizes = [self.size()]
        for subdir in self.subdirs.values():
            list_sizes += subdir.all_sizes()
        return list_sizes

    def __repr__(self):
        return self.name


root = Directory("/", None)
current_dir = None

with open("input7.txt", "r") as f:
    for line in f:
        if line.startswith("$"):
            parts = line.strip().split()
            if parts[1] == "cd":
                if parts[2] == "/":
                    current_dir = root
                elif parts[2] == "..":
                    current_dir = current_dir.upper
                else:
                    current_dir = current_dir.subdirs[parts[2]]
            elif parts[1] == "ls":
                pass
            else:
                raise ValueError("unknown input")
        else:
            size, name = line.strip().split()
            if size == "dir":
                current_dir.add_dir(name)
            else:
                current_dir.add_file(int(size), name)

result = 0
for size in root.all_sizes():
    if size <= 100000:
        result += size
print(result)
