#!/bin/bash
rm last_updated.txt
db = new Mongo().getDB("users");
db.dropDatabase();
