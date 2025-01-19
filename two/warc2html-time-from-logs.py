import re
import sys
import fire

def convert_to_seconds(time_str):
    hours, minutes, seconds = map(int, re.findall(r'(\d+)h(\d+)m(\d+)s', time_str)[0])
    return hours * 3600 + minutes * 60 + seconds


def main():
    t = [convert_to_seconds(l.strip()) for l in sys.stdin]
    print(len(t), sum(t))        

fire.Fire(main)
