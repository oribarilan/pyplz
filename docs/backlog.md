## Features

| feature                    | implemented | tested | doced |
| -------------------------- | ----------- | ------ | ----- |
| env dotenv                 | v           | v      | v     |
| env task definition        | v           | v      | v     |
| env in-line                | v           | v      | v     |
| env config                 |             |        |       |
| plz declare file type (-f) |             |        |       |
| list                       | v           |        |       |
| default                    | v           | v      |       |
| help                       | v           |        | v     |
| dependencies               | v           | v      | v     |
| plz.run with *args         | v           | v      | v     |
| verbosity                  |             |        |       |

## Should
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