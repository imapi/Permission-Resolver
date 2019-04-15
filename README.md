# Permission Resolver
## Task
Given lists of readable and writable absolute paths return tree like hierarchical structure where all leafs 
are writable folders and all parent nodes are writable or readable.

## Solution
Permission resolver application accepts text files with readable and writable folders lists and stdout the required
output structure. Posix or Windows like paths both supported. Files of readable and writable folders expected to be
newline terminated (one path per line).

### Environment
Python 3.6 should be installed

### How to use
Using provided sample fixture files:
```bash
     python -m permission_resolver -r "tests/fixtures/read_1" "tests/fixtures/read_2" -w "tests/fixtures/write_1"
```

List all available options:
```bash
     python -m permission_resolver -h
```