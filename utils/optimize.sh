mkdir optimized
i=1
for file in *.jpg; do
  convert "$file" -units PixelsPerInch -density 72 -quality 85 "optimized/$i.jpg"
  let i++
done