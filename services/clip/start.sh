CONTAINER_NAME="clip"
CONTAINER_IMG="expert-seek:clip"
PORT=8001

sudo docker run \
    -it \
    --rm \
    -p $PORT:$PORT \
    --name $CONTAINER_NAME \
    $CONTAINER_IMG