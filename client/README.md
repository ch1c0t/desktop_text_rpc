# Desktop Text RPC — Crystal client

This small CLI uses [crystal.hobby-rpc.client](https://github.com/ch1c0t/crystal.hobby-rpc.client)
to call the service over its Unix domain socket.

## Build

Requires Crystal 1.21 or newer and Shards.

```sh
cd client
shards install
shards build
```

## Try it

Start the Python service in another terminal:

```sh
uv run desktop-text-rpc serve
```

Search the primary display for text:

```sh
./bin/desktop-text-rpc-client present "Press a key" --display :1
```

Recognize and print all text from a display:

```sh
./bin/desktop-text-rpc-client recognize --display :1
```

The socket defaults to `~/.local/share/desktop-text-rpc/socket`. Override it
with `--socket /path/to/socket` or `DESKTOP_TEXT_RPC_SOCKET`. If `--display`
is omitted, the server's `DISPLAY` environment variable is used.
The `present` command returns the JSON result, including `found`, `matches`,
and recognized `lines`; `recognize` returns all recognized lines.
