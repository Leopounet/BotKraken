#!/bin/bash
command_file="commands.cmd"
rcv_command_file="/home/ubuntu/BotKrakenCommands/commands.cmd"

git -C ~/BotKrakenCommands/ pull

if [[ ! -f "$command_file" ]]; then
	touch "$command_file"
fi

to_write=()

while IFS= read -r line; do
	if [[ "$line" =~ "[".* ]]; then
		to_write+=("$line")
	else
		if [[ "$line" = "START" ]]; then
			to_write+=("[$(date +%F_%H-%M-%S)] $line")
			python3 main.py &
		else
			echo "$line" >> $command_file
			to_write+=("[$(date +%F_%H-%M-%S)] $line")
		fi
	fi
done < "$rcv_command_file"

for line in "${to_write[@]}"; do
	echo "$line" > $rcv_command_file
done

line=~/BotKrakenCommands/
git -C "$line" rm --cached "$line/*" > /dev/null 2>&1
git -C "$line" add "$line/*"
git -C "$line" add -u
git -C "$line" commit -m "Auto-push!"
git -C "$line" push
