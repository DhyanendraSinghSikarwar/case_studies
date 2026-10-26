#!/bin/sh
# usage: run_spark.sh script.py   (venv from the Part 9 setup; JAVA_TOOL_OPTIONS noise filtered)
/tmp/claude-0/b9p09/spark/bin/python -I "$1" 2>&1 | grep -v "JAVA_TOOL_OPTIONS\|WARNING: Using incubator\|^WARNING\|Setting default log level\|To adjust logging\|NativeCodeLoader\|WARN \|log4j"
