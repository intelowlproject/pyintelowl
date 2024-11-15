# Checklist for creating a new release

- [ ] I have already checked if all Dependabot issues have been solved before creating this PR.
- [ ] Verify that this PR is for `master` branch from the `develop` branch.
- [ ] Update `CHANGELOG.md` for the new version
- [ ] Change version number in `pyintelowl/version.py`. This is the version number that will be used to create the package later.
- [ ] Verify CI Tests
- [ ] Merge the PR to the `master` branch. **Note:** Only use "Merge and commit" as the merge strategy and not "Squash and merge". Using "Squash and merge" makes history between branches misaligned.
- [ ] Create a New Release named with the version number. An action would automatically create and upload the package on Pypi.


