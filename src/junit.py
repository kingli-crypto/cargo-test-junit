#!python3
import fileinput
import re
import sys

##########################################################################################
def match_all_tests(test_input):
    matches = re.findall(r'^test ([^ ]+) ... (\w+)$', test_input, re.M)
    return [(a[0], a[1], discover_output(test_input, a[0])) for a in matches]

def discover_output(test_input, name):
    return re.findall(r'---- ' + name + ' (.+?) ----\n(.+?\n)\n', test_input, re.DOTALL)

##########################################################################################
def junit_failure(details):
    type_failure, details = details
    return f"""<failure type="{type_failure}">\n{details}</failure>"""

def junit_line(entry):
    name, result, details = entry
    if result in ["ok", "OK", "PASS", "pass"]:
        return f"""<testcase classname="Cargo" name="{name}"/>"""
    elif result in ["FAILED", "FAIL"]:
        failures = "\n".join([junit_failure(x) for x in details])
        return f"""<testcase classname="Cargo" name="{name}">\n{failures}\n</testcase>"""
    elif result in ["ignored", "IGNORED"]:
        return f"""<!--{name} ignored-->"""
    else:
        raise NotImplementedError(f"Type {result} is not implemented ({name})")

def junit_output(output):
    lines = "\n".join([junit_line(x) for x in output])
    return f"""<testsuite tests="{len(output)}">\n{lines}\n</testsuite>"""

##########################################################################################
if __name__ == "__main__":
    input_all = "".join([line for line in sys.stdin])
    matched_results = match_all_tests(input_all)
    print(f"Found {len(matched_results)} tests")
    output = junit_output(matched_results)

    with open(sys.argv[1], 'w+') as f:
        print(output, file=f)