# Hypermedia Demo

A demonstration of an important benefit of clients following the hypermedia constraint.

This repo is a companion to this video:  [Hypermedia Constraint](https://app.cri.com/images/HypermediaConstraint.mp4)

## Contents

* `server-before` - this folder contains the implementation of the resource model as a single API called catalog-api
* `server-after` - this folder contains the implementation of the same resource model, but as multiple APIs using the Gateway pattern
* `clients`
  * `populate` - this folder contains a script ( `full_pop.py` ) to populate the data when you spin up each API for the first time with an empty database
  * `good` - a simple client application ( `report.py` ) which reports on that data, following the hypermedia constraint, and thus works with any version of the server as long as server-side fulfils its hypermedia constraint obligations
  * `bad`
    * a simple client application ( `report.py` ) which reports on that data, but only works with `server-before`
    * a second version of the client application ( `report-after.py` ) which shows how the first version needed to be refactored together with the server-side refactor.  It only works with `server-after`

