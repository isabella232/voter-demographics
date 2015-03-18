# voter-demographics

## Getting the data

```
curl -O http://thedataweb.rm.census.gov/pub/cps/supps/nov12pub.zip
unzip nov12pub.zip
in2csv -s schema.csv nov12pub.dat > nov12pub.csv
```

## Sources

* [CPS Data Download FTP](http://thedataweb.rm.census.gov/ftp/cps_ftp.html)
* [National Bureau of Economic Research schema files for CPS data](http://www.nber.org/data/cps_progs.html)

## Documentation

* [Census Bureau Docs for CPS Voter Supplement](http://www.census.gov/prod/techdoc/cps/cpsnov12.pdf)
