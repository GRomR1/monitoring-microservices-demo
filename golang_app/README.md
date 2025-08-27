# Golang App

A simple golang web app that returns json on request to `/albums`. Does not contain any additional dependencies for instrumentation. The app is used with eBPF instrumentation via [Beyla](https://grafana.com/oss/beyla-ebpf/).

## Environment vars

None

# Running

Simple running only web-server (without instrumentation)
```sh
$ go run .
2025/08/27 10:31:13 Server is running on port:8002
```

# Testing

Run http-request via curl command after running application.
```sh
❯ curl localhost:8002/albums
[{"id":"1","title":"Blue Train","artist":"John Coltrane","price":56.99},{"id":"2","title":"Jeru","artist":"Gerry Mulligan","price":17.99},{"id":"3","title":"Sarah Vaughan and Clifford Brown","artist":"Sarah Vaughan","price":39.99}]
```

The application will show next logs (request headers):
```
...
2025/08/27 10:32:08 New request /albums
2025/08/27 10:32:08   Request Headers:
2025/08/27 10:32:08   - User-Agent: curl/8.7.1
2025/08/27 10:32:08   - Accept: */*
```