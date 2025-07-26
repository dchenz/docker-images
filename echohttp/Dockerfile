ARG GOLANG_BASE_IMAGE

FROM golang:${GOLANG_BASE_IMAGE} AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o app .

FROM scratch

COPY --from=builder /app/app /app

ENTRYPOINT ["/app"]
