jq -c -r '[.scores,(.text|split("\n")|map(length),map(utf8bytelength),.)]|transpose|.[]|join("\t")'
