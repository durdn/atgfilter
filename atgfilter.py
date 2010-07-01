#!/usr/bin/env python
import sys
import logging
import re

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

patterns = {'(Include)' : BLUE,
            '(<IfModule.*>)': MAGENTA,
            '(configuration\s\W?)': RED,
            '(?<=ErrorDocument)\s(\d\d\d)': CYAN,
            '(?<=ErrorDocument\s\d\d\d)\s(.*)': GREEN,
            '(ErrorDocument)': YELLOW,
            }

def colorize(str,color,bold = False):
    color_code = COLOR_SEQ % (30 + color)
    colored = "%s%s%s%s" % (BOLD_SEQ if bold else '', color_code,str,RESET_SEQ)
    return colored


if __name__ == '__main__':
    while 1:
        line = sys.stdin.readline()
        per_line_matches = {}
        for p in patterns:
            match = re.search(p,line)
            if match:
                try:
                    group = match.groups()[0]
                    per_line_matches[group] = colorize(group, patterns[p])
                except IndexError:
                    pass
        for m in per_line_matches.keys():
            line = line.replace(m,per_line_matches[m])
        if not line:
            break
        sys.stdout.write(line)
        
