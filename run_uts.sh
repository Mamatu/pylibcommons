#!/bin/bash
PYTHONPATH=.. python3 -m pytest $(find -name "ut_*.py")
