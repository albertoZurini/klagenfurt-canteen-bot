xhost +;
docker run -v $PWD:/app \
--env DISPLAY=unix$DISPLAY  \
--volume /tmp/.X11-unix:/tmp/.X11-unix \
--rm \
--privileged \
-p 5678:5678 \
-it selenium:dev \
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client send_screen.py