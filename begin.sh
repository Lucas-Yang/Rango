echo "######################"
echo `pwd`
run_env=$1
echo "$run_env"
if [ "$run_env" = "prod" ]
then
  # shellcheck disable=SC2164
  cd /data/app/rango
  cp -r /data/app/rango/config/prodconfig.py /data/app/rango/config/config.py
  python /data/app/rango/main.py --reload=False & /home/work/.local/bin/celery -A app.bin.tasks worker -l info
else
  cp -r config/testconfig.py config/config.py
  python main.py & celery -A app.bin.tasks  worker -l info
fi