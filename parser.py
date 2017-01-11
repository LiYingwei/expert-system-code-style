import re


def count_indent(line):
    tab = 0
    space = 0
    for char in line:
        if char in "\t":
            tab += 1
        elif char in " ":
            space += 1
        else:
            return tab, space
    return tab, space


def parser(file):
    global_facts = {}
    line_facts = list()

    with open(file, 'rw') as f:
        lines = f.read()
    lines = re.sub(r'((?<=\n)|^)[ \t]*\/\*.*?\*\/\n?|\/\*.*?\*\/|((?<=\n)|^)[ \t]*\/\/[^\n]*\n|\/\/[^\n]*', '', lines)
    lines = lines.split('\n')

    tab_count = 0
    space4_count = 0
    new_line_left_brace = 0
    end_line_left_brace = 0
    for line in lines:
        tab, space = count_indent(line)
        line = line.strip()
        if len(line) == 0:
            continue
        facts = dict()
        facts["begin with"] = line[0]
        facts["end with"] = line[-1]
        facts["tab"] = tab
        facts["space"] = space / 4
        line_facts.append(facts)

        if tab > 0:
            tab_count += 1
        if space > 0:
            space4_count += 1
        if line[0] == '{':
            new_line_left_brace += 1
        elif line[-1] == '{':
            end_line_left_brace += 1

    if tab_count > space4_count:
        global_facts["indentation"] = "tab"
    else:
        global_facts["indentation"] = "space"
    if new_line_left_brace > end_line_left_brace:
        global_facts["{ at"] = "a new line"
    else:
        global_facts["{ at"] = "the end of a line"

    for facts in line_facts:
        if global_facts["indentation"] == "tab":
            if facts["space"] != 0:
                facts["tab"] += facts["space"]
                facts["space"] = 0
                facts["indent wrong"] = True
        else:
            if facts["tab"] != 0:
                facts["space"] += facts["tab"]
                facts["tab"] = 0
                facts["indent wrong"] = True

    return global_facts, line_facts
