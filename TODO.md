## TODO

**Description**
In Test folder the `test.py` contains the algorithm used to check which versions of the packages are vulnerable given the vulnerable version range. This code should be placed in `vulnerability_checker.py`

**List TODO**:
- Add the case that the version range is `1.x` or `1.0.x`
- Add the case that the version range is *
- Check if there is a better way to check the version range * because in some cases the npm audit
generates false result idincating that the verion range is *. However in the github advisory the vulnerable range version is different (updated)