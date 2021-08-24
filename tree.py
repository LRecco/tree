#!/usr/bin/env python3
import os, time, sys
from pathlib import Path
sys.setrecursionlimit(1500) # Increase recursion limit to allow entire drives to be recursed through


class FileTree:
    def __init__(self, starting_dir: str) -> None:
        """
        A tree structure of all directories and subdirectories 
        from the starting directory (starting_dir).
        """
        self.starting_dir = starting_dir

    def get_parent(self, dir: str):
        """
        Get the parent directory for the given directory. 
        The equivalent of '../' in linux.
        """
        relative_parent = os.path.join(dir, "..")
        return os.path.abspath(relative_parent)

    def get_child_count(self, dir: str):
        """
        Returns the amount of parent folders from the 
        given directory to the starting directory.
        """
        if Path(dir) in Path(self.starting_dir).parents:
            return 0

        count = 0
        while (parent := self.get_parent(dir) + "\\") != self.starting_dir + "\\":
            count += 1
            dir = parent
        return count

    def print(self, dir: str):
        """
        Prints all directories and subdirectories of the 
        given directory, in a tree like structure.
        """
        count = 0    
        if os.path.exists(dir) and os.path.isdir(dir):
            for root, dirs, files in os.walk(dir):
                # Skip system folders such as the $Recycle.Bin
                if "$" in root:
                    continue
                # Had to pass a fake child directory to get the correct
                # child count outside of the nested for loop
                child_count = self.get_child_count(root + "\\a")
                print("  " * child_count + root)
                for file in files:
                    fullpath = os.path.join(root, file)
                    child_count = self.get_child_count(fullpath)
                    count += 1
                    if os.path.isdir(fullpath):
                        print(("  " * child_count) + fullpath)
                    else:
                        print("  " * (child_count) + "|____" + fullpath)
        return count


def parse_arguments() -> list[str]:
    """
    Parse arguments passed to this script. 
    Returns a list of paths passed in by the user.
    """
    args = [arg for arg in sys.argv[1:]]
    return args

def show_tree(starting_dir: str) -> None:
    """
    Starts a FileTree instance for the given 
    directory and returns the file count.
    """
    tree = FileTree(starting_dir)
    file_count = tree.print(starting_dir)
    print("There were a total of {} files in {}".format(file_count, starting_dir))

def main():
    """
    Main program execution. If arguments are passed in, 
    parse them and print a tree of each path passed in.
    """
    args = parse_arguments()
    if len(args) > 0:
        for dir in args:
            show_tree(dir)
            print()
    else:
        starting_dir = os.getcwd()
        show_tree(starting_dir)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))