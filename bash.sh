git pull origin master
git add .
git commit -m "updated responsiveness to bot"
git push -f origin master
heroku git:remote -a specdrum-chat
git push -f heroku specdrum-chat:master
