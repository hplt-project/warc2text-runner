#!/bin/bash
zstdcat $1 | jq -c '. + {"lang":[[(.htmllang//["null"]|join("/")),(.u|split("/")[2]|split(".")[-1])]|join(".")], "text":.t2}'
