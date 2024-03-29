l = """
User-agent: *
Disallow: /next2/

User-agent: *
Disallow: /next1/

""".split('\n')

from urllib.robotparser import RobotFileParser
parser = RobotFileParser()
parser.parse(l)

print(parser.default_entry)

print('#entries:', len(parser.entries))
# e = parser.entries[0]
# print(e)

print(parser.can_fetch('Googlebot', 'http://a.com/next1/q'))
print(parser.can_fetch('Googlebot', 'http://a.com/next2/q'))