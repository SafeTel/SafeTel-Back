FROM golang:1.16-alpine

WORKDIR /app

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

ARG DBName=Melchior
ARG DBPassword=aSEFTHUKOM1!
ARG MongoAtlasClusterURI= mongodb+srv://SafeTelBackEndUser:${DBPassword}@safetel-back-cluster.klq5k.mongodb.net/${DBName}?retryWrites=true&w=majority

RUN go build -o Magi .

EXPOSE 2407

CMD ["./Magi"]
