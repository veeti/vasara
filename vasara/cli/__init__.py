import sys
import os
import argparse

def main():
    compiler = get_compiler()
    parser = argparse.ArgumentParser(description="A static site generator.")
    subparsers = parser.add_subparsers(dest="command")

    compile = subparsers.add_parser("compile")

    #server = subparsers.add_parser("server")
    #server.add_argument("--port", type=int, default=8000)
    #server.add_argument("--listen", type=str, default="127.0.0.1")

    args = parser.parse_args()
    if args.command == "compile":
        compiler.compile()
        print "Compiled."

# TODO: Hacky. Is there a better way to do this?
def get_compiler():
    """Attempts to import a function called get_vasara_compiler from the current working
    directory. This will be used by the command-line tools."""
    sys.path.append(os.getcwd())
    try:
        result = reload(__import__("__init__"))
        if not hasattr(result, "get_vasara_compiler"):
            raise ImportError
    except ImportError as e:
        print e
        sys.exit("A site doesn't seem to exist in the working directory. Exiting.")
    return result.get_vasara_compiler()