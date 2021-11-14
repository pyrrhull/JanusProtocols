from collections import defaultdict
from pathlib import Path

def main():
    Path(".").rglob(".MPT")
    d = defaultdict(list)

    for tpl in sorted([ (x.name, str(x.absolute())) for x in Path("C:\\Packard\\Janus\\").rglob("**/*.MPT")]):
        d[tpl[0]] = tpl[1]
    return d
if __name__ == "__main__":
    d = main()
    print(d)