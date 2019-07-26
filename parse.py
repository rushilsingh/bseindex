import textfsm
from sys import argv


def parse(text, template):
    """ Parses given text according to template and returns result """
    parsed = []
    with open(template) as f:
        parser = textfsm.TextFSM(f)

    parsed.append(parser.header)
    parsed.extend(parser.ParseText(text))
    return parsed


def main():

    template = argv[1]
    result = argv[2]

    with open(result) as f:
        text = f.read()

    print parse(text, template)


if __name__ == '__main__':
    main()
