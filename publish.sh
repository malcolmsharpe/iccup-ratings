set -e
set -x

# Since we aren't publish the games JSON now, don't generate it.
#python dump_games_json.py
cp static/leader.css ../www/static/leader.css
cp html/leaderboard.html ../www/html/leaderboard.html
# Disable games dump for now since it's not getting use.
#cp html/games.json ../www/games.json
cp html/maps.html ../www/html/maps.html
cd ../www
git commit -a -m 'Publish latest data.'
git push origin gh-pages
