CONTAINER_NAME="vectordb"
CONTAINER_IMG="expert-seek:vectordb"
PORT=8002

sudo docker run \
    -it \
    --rm \
    -p $PORT:$PORT \
    --name $CONTAINER_NAME \
    $CONTAINER_IMG