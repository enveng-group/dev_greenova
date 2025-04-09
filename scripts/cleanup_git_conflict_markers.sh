#!/bin/sh

find . -type f -not -path "*/\.git/*" -exec sed -i -e "/^<<<<<<< HEAD$/,/^=======$/d" -e "/^>>>>>>>.*$/d" {} \;
