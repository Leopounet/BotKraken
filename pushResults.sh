rm -rf ~/BotKrakenResult/*
cp -r ~/BotKraken/src/Results/* ~/BotKrakenResult/
cp -r ~/BotKraken/src/logs.txt ~/BotKrakenResult/
line=~/BotKrakenResult/
git -C "$line" rm --cached "$line/*" > /dev/null 2>&1
git -C "$line" add "$line/*"
git -C "$line" add -u
git -C "$line" commit -m "Auto-push!"
git -C "$line" push

