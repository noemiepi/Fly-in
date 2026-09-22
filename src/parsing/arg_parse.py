import argparse


def arg_parse() -> argparse.Namespace:
    """
    This function will create a few arguments the
    user can use when launching the progam.

    Return
    -> argparse.Namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--visual",
                        nargs="?",
                        const=True,
                        default=False,
                        help="Activates the arcade visual")

    parser.add_argument("-o", "--output",
                        nargs="?",
                        const=True,
                        default=False,
                        help="Creates a file storing the output")

    return parser.parse_args()
