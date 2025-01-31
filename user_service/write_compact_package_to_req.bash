#!/bin/sh
pip list --not-required | awk '{print $1}' | tail -n +3 > req.txt
