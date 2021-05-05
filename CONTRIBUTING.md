Contributing
------------

Thanks for contributing! Please pay attention to the following notices:

After cloning the repo, you will need to run `bash install.sh` from the repository root. This will setup
automatic calendar versioning for you, and also some checks on your working branch name. For avoidance of doubt,
branches must be linked to a GitHub issue and named accordingly:

```bash
{GitHub issue number}_{tinyLowerCamelDescription}
```
For example `14_readme`, which indicates that [this branch](https://github.com/nestauk/ojd_daps/pull/24) refered to [this issue](https://github.com/nestauk/ojd_daps/issues/14).

The remote repo anyway forbids you from pushing directly to the `dev` branch, and the local repo will forbid you from committing to either `dev` or `master`, and so you only pull requests from branches named `{GitHub issue number}_{tinyLowerCamelDescription}` will be accepted.

Please make all PRs and issues reasonably small: they should be trying to achieve roughly one task. Inevitably some simple tasks spawn large numbers of utils, and sometimes these detract from the original PR. In this case, you should stack an new PR on top of your "base" PR, for example as `{GitHub issue number}_{differentLowerCamelDescription}`. In this case the PR / Git merging tree will look like:

    dev <-- 123_originalThing <-- 423_differentThing <-- 578_anotherDifferentThing
    
We can then merge the PR `123_originalThing` into `dev`, then `423_differentThing` into `dev` (after calling `git merge dev` on `423_differentThing`), etc until the chain is merged entirely. The nominated reviewer should review the entire chain, before the merge can go ahead. PRs should only be merged if all tests and a review has been signed off.
