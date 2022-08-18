#!/usr/bin/env bash
while getopts a:n:u:d: flag
do
    case "${flag}" in
        a) author=${OPTARG};;
        n) name=${OPTARG};;
        u) urlname=${OPTARG};;
        d) description=${OPTARG};;
    esac
done

echo "Author: $author";
echo "Project Name: $name";
echo "Project URL name: $urlname";
echo "Description: $description";

echo "Renaming project..."

original_author="pappacena"
original_name="asyncio_inspector"
original_urlname="asyncio-inspector"
original_description="Awesome asyncio_inspector created by pappacena"
# for filename in $(find . -name "*.*") 
for filename in $(git ls-files) 
do
    sed -i "s/$original_author/$author/g" $filename
    sed -i "s/$original_name/$name/g" $filename
    sed -i "s/$original_urlname/$urlname/g" $filename
    sed -i "s/$original_description/$description/g" $filename
    echo "Renamed $filename"
done

mv asyncio_inspector $name

# This command runs only once on GHA!
if [ -f .github/workflows/asyncio_inspector.yml ]; then
    mv .github/workflows/rename_project.yml .github/workflows/rename_project.yml.disabled
fi
