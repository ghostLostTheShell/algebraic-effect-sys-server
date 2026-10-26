# Effect Server

## 启动开发服务器

使用 Poetry 在项目虚拟环境中启动 Granian：

```bash
poetry run granian --interface asgi effect-server.http:app
```

服务默认监听 `http://127.0.0.1:8000`。
