#!/bin/bash

# Define a function to process a single item
process_item() {
  # some command to process the item
  echo "Processing ${1}"
  # simulate some work
  sleep 1
}
# Export the function to the environment
export -f process_item
# Create a list of items to process
items=(1 2 3 4 5 6 7 8 9 10)

# Use parallel to process the items in parallel
parallel -j 100 process_item ::: "${items[@]}"

