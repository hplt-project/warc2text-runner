find ./ -name 'text.gz' -print0 | du -b --files0-from=- > sizes

