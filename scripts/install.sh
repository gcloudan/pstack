#!/bin/sh
set -eu
kit_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skills_root=${HOME}/.cursor/skills
replace_existing=false
while [ "$#" -gt 0 ]; do
    case "$1" in
        --skills-root) [ "$#" -ge 2 ] || { echo 'Missing --skills-root path' >&2; exit 1; }; skills_root=$2; shift 2 ;;
        --replace-existing) replace_existing=true; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
done
mkdir -p "$skills_root"
skills_root=$(CDPATH= cd -- "$skills_root" && pwd)
backup_root="$(dirname -- "$skills_root")/work-style-backups/$(date +%Y%m%dT%H%M%S)-$$"
conflicts=false
for skill in automate-me work-mode repo-onboarding; do
    source_file="$kit_root/skills/$skill/SKILL.md"
    destination_file="$skills_root/$skill/SKILL.md"
    [ -f "$source_file" ] || { echo "Missing kit file: $source_file" >&2; exit 1; }
    if [ -e "$destination_file" ]; then
        if cmp -s "$source_file" "$destination_file"; then
            echo "Already current: $skill"
            continue
        fi
        if [ "$replace_existing" = false ]; then
            echo "Preserved existing $skill. Compare before using --replace-existing." >&2
            conflicts=true
            continue
        fi
        mkdir -p "$backup_root/$skill"
        cp "$destination_file" "$backup_root/$skill/SKILL.md"
        echo "Backed up: $skill to $backup_root/$skill"
    fi
    mkdir -p "$skills_root/$skill"
    cp "$source_file" "$destination_file"
    echo "Installed: $skill to $destination_file"
done
[ "$conflicts" = false ] || exit 2
echo 'Skills installed. Activate work-mode separately using docs/cursor-user-rule.txt.'
