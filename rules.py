from copy import deepcopy


def reserve_rule(rule):
    ret = deepcopy(rule)
    for index, previous_key in enumerate(ret[0]):
        (key, value) = previous_key
        if value.startswith("not "):
            [_, value] = value.split("not ", 1)
        else:
            value = "not " + value
        ret[0][index] = (key, value)

    if ret[1] in "and":
        ret[1] = "or"
    else:
        ret[1] = "and"

    if ret[2][1].startswith("not "):
        value = ret[2][1].split("not ", 1)
    else:
        value = "not " + ret[2][1]
    ret[2] = (ret[2][0], value)

    return ret


rules = list()

complete_line_rule = [
    [("previous line end with", ";"), ("previous line end with", "}"), ("previous line begin with", "#")],
    "or",
    ("previous line is a complete sentence", "True")]

rules.append(complete_line_rule)
rules.append(reserve_rule(complete_line_rule))
rules.append([[("previous line is not exist", "True")],
              "and",
              ("indent should", "0")])
rules.append([[("previous line is a complete sentence", "True"), ("this line begin with", "}")],
              "and",
              ("indent should", "-1")])
rules.append([[("previous line is a complete sentence", "True"), ("this line begin with", "not }")],
              "and",
              ("indent should", "0")])
rules.append([[("previous line is a complete sentence", "False"), ("this line begin with", "{")],
              "and",
              ("indent should", "0")])
rules.append([[("previous line is a complete sentence", "False"), ("this line begin with", "not {")],
              "and",
              ("indent should", "1")])
rules.append([[("previous line is a complete sentence", "False"), ("previous line end with", "not {"), ("this line begin with", "not {")],
              "and",
              ("next indent should", "-1")])
rules.append([[("{ at", "a new line"), ("this line begin with", "not {"), ("this line end with", "{")],
               "and",
               ("{ should in a new line", "True")])
rules.append([[("{ at", "the end of a line"), ("this line begin with", "{")],
               "and",
               ("{ should follow in a line", "True")])
rules.append([[("this line begin with", "{"), ("this line end with", "not {")],
              "and",
              ("{ should take an entire line", "True")])
rules.append([[("this line begin with", "not }"), ("this line end with", "}")],
              "and",
              ("} should take an entire line", "True")])