# Checklist for creating a new release

- [ ] Update `CHANGELOG.md` for the new version
- [ ] Change version number in `pyintelowl/version.py`
- [ ] Verify CI Tests
- [ ] Verify that this PR is for `master` branch from the `develop` branch and that is called with the version number. Example: "5.1.0". This is important because this value is used to auto-build the pyintelowl package and push it in Pypi.
- [ ] Merge the PR to the `master` branch. **Note:** Only use "Merge and commit" as the merge strategy and not "Squash and merge". Using "Squash and merge" makes history between branches misaligned.


