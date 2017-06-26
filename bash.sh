git pull origin master
git add .
git commit -m "updated responsiveness to bot"
git push -f origin master
git push heroku specdrum-chat:master
heroku logs
