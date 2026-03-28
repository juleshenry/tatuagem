#!/bin/bash

# GitHub Activity Generator - Superhero Edition
# Creates random commits in THIS repo to make your contribution graph look active

COMMITS_PER_DAY="${COMMITS_PER_DAY:-5}"
DAYS_BACK="${DAYS_BACK:-365}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Superhero Activity Generator${NC}"
echo "Generating $COMMITS_PER_DAY commits/day for $DAYS_BACK days..."

for ((day=DAYS_BACK; day>=0; day--)); do
    num_commits=$((RANDOM % (COMMITS_PER_DAY + 1)))
    
    if [ $num_commits -gt 0 ]; then
        commit_date=$(date -d "$day days ago" +%Y-%m-%d)
        
        for ((c=0; c<num_commits; c++)); do
            hour=$((RANDOM % 24))
            minute=$((RANDOM % 60))
            second=$((RANDOM % 60))
            
            git_date="$commit_date $hour:$minute:$second"
            export GIT_AUTHOR_DATE="$git_date"
            export GIT_COMMITTER_DATE="$git_date"
            
            filename="hero_$((RANDOM % 50)).json"
            echo "{\"power\": $RANDOM, \"date\": \"$git_date\"}" > "$filename"
            
            git add "$filename"
            git commit -m "🦸 $git_date" > /dev/null 2>&1
            echo -e "${GREEN}[+]${NC} $git_date"
        done
    fi
done

echo -e "\n${YELLOW}Done! Push with: git push -u origin main --force${NC}"
