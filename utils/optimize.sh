#!/bin/bash

mkdir -p optimized
i=1
target_size=1000000  # target size in bytes (1MB)
tolerance=100000     # tolerance in bytes (100KB)

for file in *.jpg; do
    quality=85
    step=2
    while true; do
        convert "$file" -units PixelsPerInch -density 72 -quality $quality "optimized/$i.jpg"
        actual_size=$(stat -c%s "optimized/$i.jpg")

        if [ $actual_size -le $((target_size + tolerance)) ] && [ $actual_size -ge $((target_size - tolerance)) ]; then
            break
        elif [ $actual_size -lt $((target_size - tolerance)) ]; then
            quality=$((quality + step))
        else
            quality=$((quality - step))
        fi

        # Prevent infinite loop
        if [ $quality -le 0 ] || [ $quality -ge 100 ]; then
            break
        fi
    done
    i=$((i + 1))
done