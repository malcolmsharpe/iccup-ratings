set -e
set -x

python dump_games_json.py
cp static/leader.css ../www/static/leader.css
cp html/leaderboard.html ../www/html/leaderboard.html
cp html/games.json ../www/games.json
cp html/maps.html ../www/html/maps.html
cd ../www
git commit -a -m 'Publish latest data.'
git push origin gh-pages