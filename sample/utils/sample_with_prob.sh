#!/bin/bash

PROB=$1
perl -ne 'print if (rand() < '$PROB')'
