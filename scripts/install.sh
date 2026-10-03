#!/bin/sh
set -eu
kit_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skills_root=${HOME}/.cursor/skills
agents_root=
workspace_root=
custom_roots=false
replace_existing=false
dry_run=false
while [ "$#" -gt 0 ]; do
    case "$1" in
        --skills-root) [ "$#" -ge 2 ] || { echo 'Missing --skills-root path' >&2; exit 1; }; skills_root=$2; custom_roots=true; shift 2 ;;
        --agents-root) [ "$#" -ge 2 ] || { echo 'Missing --agents-root path' >&2; exit 1; }; agents_root=$2; custom_roots=true; shift 2 ;;
        --workspace-root) [ "$#" -ge 2 ] || { echo 'Missing --workspace-root path' >&2; exit 1; }; workspace_root=$2; shift 2 ;;
        --replace-existing) replace_existing=true; shift ;;
        --dry-run) dry_run=true; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
done
if [ -n "$workspace_root" ]; then
    [ "$custom_roots" = false ] || { echo 'Use workspace root or custom roots, not both.' >&2; exit 1; }
    skills_root="$workspace_root/.cursor/skills"
    agents_root="$workspace_root/.cursor/agents"
fi
[ -n "$agents_root" ] || agents_root="$(dirname -- "$skills_root")/agents"
if [ "$(basename -- "$skills_root")" != skills ] || [ "$agents_root" != "$(dirname -- "$skills_root")/agents" ]; then
    echo 'Use adjacent skills and agents directories: the investigator resolves ../skills. No files written.' >&2
    exit 1
fi
backup_root="$(dirname -- "$skills_root")/pstack-harness-backups/$(date +%Y%m%dT%H%M%S)-$$"
conflicts=false
valid_name() {
    case "$1" in ''|*[!a-z0-9-]*|-*|*-|*--*) echo "Invalid profile name: $1" >&2; exit 1 ;; esac
}
copy_file() {
    if [ -f "$2" ] && cmp -s "$1" "$2"; then return; fi
    if [ -e "$2" ]; then
        mkdir -p "$(dirname -- "$3")"
        cp "$2" "$3"
        echo "Backed up: $3"
    fi
    mkdir -p "$(dirname -- "$2")"
    cp "$1" "$2"
}
package_current() (
    file_list=$(find "$1" -type f)
    while IFS= read -r source_file; do
        relative=${source_file#"$1"/}
        destination_file="$2/$relative"
        if [ ! -f "$destination_file" ] || ! cmp -s "$source_file" "$destination_file"; then exit 1; fi
    done <<EOF
$file_list
EOF
)
while IFS= read -r skill || [ -n "$skill" ]; do
    valid_name "$skill"
    source_dir="$kit_root/skills/$skill"
    destination_dir="$skills_root/$skill"
    [ -f "$source_dir/SKILL.md" ] || { echo "Missing skill: $skill" >&2; exit 1; }
    if package_current "$source_dir" "$destination_dir"; then echo "Already current: skill:$skill"; continue; fi
    if [ -e "$destination_dir" ] && [ "$replace_existing" = false ]; then
        echo "Preserved differing skill:$skill; compare before replacement." >&2
        conflicts=true
        continue
    fi
    if [ "$dry_run" = true ]; then echo "Would install: skill:$skill"; continue; fi
    file_list=$(find "$source_dir" -type f)
    while IFS= read -r source_file; do
        relative=${source_file#"$source_dir"/}
        copy_file "$source_file" "$destination_dir/$relative" "$backup_root/skills/$skill/$relative"
    done <<EOF
$file_list
EOF
    echo "Installed: skill:$skill"
done < "$kit_root/profiles/core.skills"
install_single() {
    if [ -f "$2" ] && cmp -s "$1" "$2"; then echo "Already current: $4"; return; fi
    if [ -e "$2" ] && [ "$replace_existing" = false ]; then
        echo "Preserved differing $4; compare before replacement." >&2
        conflicts=true
        return
    fi
    if [ "$dry_run" = true ]; then echo "Would install: $4"; return; fi
    copy_file "$1" "$2" "$3"
    echo "Installed: $4"
}
while IFS= read -r agent || [ -n "$agent" ]; do
    valid_name "$agent"
    install_single "$kit_root/agents/$agent.md" "$agents_root/$agent.md" "$backup_root/agents/$agent.md" "agent:$agent"
done < "$kit_root/profiles/core.agents"
if [ -n "$workspace_root" ]; then
    install_single "$kit_root/rules/pstack-harness.mdc" "$workspace_root/.cursor/rules/pstack-harness.mdc" "$backup_root/rules/pstack-harness.mdc" 'rule:pstack-harness'
fi
[ "$conflicts" = false ] || exit 2
if [ "$dry_run" = true ]; then
    echo 'Preview complete; no files written.'
elif [ -n "$workspace_root" ]; then
    echo 'Core installed with a namespaced project rule. Existing harness files retained.'
else
    echo 'Core installed. User activation text is in docs/cursor-user-rule.txt.'
fi
