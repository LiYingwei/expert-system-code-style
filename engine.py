# coding=utf-8
def logic_equal(A, B):
    (AL, AR) = A
    (BL, BR) = B
    if AL != BL:
        return False
    flip = False
    if AR.startswith("not "):
        [_, AR] = AR.split("not ", 1)
        flip = not flip
    if BR.startswith("not "):
        [_, BR] = BR.split("not ", 1)
        flip = not flip
    if AR != BR:
        return flip
    else:
        return not flip


def is_fact(previous_key, facts):
    for fact, value in facts.iteritems():
        if logic_equal(previous_key, (fact, value)):
            return True
    return False


def check(rule, facts):
    if rule[1] in "and":
        for previous_key in rule[0]:
            if not is_fact(previous_key, facts):
                return False
        if is_fact(rule[2], facts):
            return False
        return True
    elif rule[1] in "or":
        if is_fact(rule[2], facts):
            return False
        for previous_key in rule[0]:
            if is_fact(previous_key, facts):
                return True
        return False
    raise NotImplemented


def forward(facts, rules):
    facts_size = -1
    while facts_size < len(facts):
        facts_size = len(facts)
        for rule in rules:
            if check(rule, facts):
                facts[rule[2][0]] = rule[2][1]
    return facts
    # return [fact for fact in facts if "should" in fact]


def solver(glb_fct, line_fct, rules):
    facts = []
    for line_num, this_line in enumerate(line_fct):
        if line_num == 0:
            previous_line = {"is not exist": "True"}
        else:
            previous_line = line_fct[line_num - 1]
        fct = {}
        for key, value in previous_line.iteritems():
            fct["previous line %s" % key] = value

        for key, value in this_line.iteritems():
            fct["this line %s" % key] = value

        for key, value in glb_fct.iteritems():
            fct[key] = value

        # print fct
        fact = forward(fct, rules)
        facts.append(fact)
        # print line_num, comment

    return facts
