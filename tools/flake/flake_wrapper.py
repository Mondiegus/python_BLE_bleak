from flake8.main.cli import main
import sys


if __name__ == "__main__":
    sys.argv = sys.argv[:]
    sys.exit(main())
