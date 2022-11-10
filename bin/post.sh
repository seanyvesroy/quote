#!/bin/sh

http --verbose POST localhost:5000/quotes/ @"$1"
