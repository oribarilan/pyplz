## Features

| feature                    | implemented | tested | doced |
| -------------------------- | ----------- | ------ | ----- |
| env dotenv                 | v           | v      | v     |
| env task definition        | v           | v      | v     |
| env in-line                | v           | v      | v     |
| env config                 | v           | v      | v     |
| plz declare file path (-f) |             |        |       |
| list                       | v           |        |       |
| default                    | v           | v      |       |
| help                       | v           |        | v     |
| dependencies               | v           | v      | v     |
| plz.run with *args         | v           | v      | v     |
| verbosity                  |             |        |       |
| ask                        | v           |        |       |

## Should
- [ ] bug - double tasks in PR (both push and pull_request), which is not needed
- [x] doc pages
- [x] move to toml based setup
- [x] CI with test
- [ ] CI with test coverage
- [x] CD
- [x] badges
- [ ] work on coverage
- [ ] bug of trace when command fails (1 output in white, 1 output in red, then long traceback)
- [ ] convert _ to - in task names
- [ ] what's new (changelog) + versioning
- [ ] testable examples in docs

### Could
- [ ] heirachial loading
- [ ] `plz .create-demo`
- [ ] async commands
- [ ] `plz.progress`
- [ ] support options for commands
- [ ] "Did you mean?" offer another command if something resembles it.