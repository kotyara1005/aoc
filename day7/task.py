TEST = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


from collections import defaultdict

PARENT = "$PARTNT"
SIZE = "$SIZE"


def new_node(parent=None):
    node = defaultdict(new_node)
    node[PARENT] = parent
    node[SIZE] = 0
    return node


def main(lines):
    st = []

    dirs = {}

    for line in lines:
        if line == "$ cd ..":
            st.pop()
        elif line.startswith("$ cd "):
            name = line[5:]
            st.append(name)
            dirs.setdefault('/'.join(st), {"size": 0, "dirs": []})
        elif line == "$ ls":
            pass
        elif line.startswith("dir "):
            key = '/'.join(st)
            dirs[key]["dirs"].append(key + '/' + line[4:])
        else:
            key = '/'.join(st)
            dirs[key]["size"] += int(line.split(" ")[0])

    def total_size(name):
        d = dirs[name]
        if "total" in d:
            return d["total"]

        d["total"] = d["size"] + sum(map(total_size, d["dirs"]))
        return d["total"]

    for name in dirs:
        total_size(name)
        print(name, total_size(name))

    free_space = 70000000 - dirs["/"]["total"]
    need_space = 30000000 - free_space
    print("free_space", free_space)
    print("need_space", need_space)
    print(min(((d["total"], k) for k, d in dirs.items() if d["total"] >= need_space)))
    return sum(d["total"] for d in dirs.values() if d["total"] < 100000)


if __name__ == '__main__':
    # assert main(TEST.splitlines()) == 95437
    print(main(open("input").read().splitlines()))
