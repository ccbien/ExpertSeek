CONTAINER_NAME="sql"

CONTAINER_IMG="expert-seek:sql"
PORT=8000

sudo docker run \
    -it \
    --rm \
    -p $PORT:$PORT \
    --name $CONTAINER_NAME \
    $CONTAINER_IMG
