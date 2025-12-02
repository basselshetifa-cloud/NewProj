# 🔥 Hybrid Cookie Checker

A high-performance cookie checker combining **Go** (speed) and **Python** (stealth) with gRPC communication and OpenBullet-style visual config editor.

## Features

✅ **Hybrid Architecture**: Go backend + Python frontend  
✅ **gRPC Communication**: Fast inter-process communication  
✅ **Visual Config Editor**: OpenBullet-style block-based editor  
✅ **Multi-format Support**: JSON, Netscape, Header cookies  
✅ **Stealth Mode**: Playwright with anti-detection  
✅ **Multi-threading**: Check thousands of cookies concurrently  
✅ **Proxy Support**: HTTP/HTTPS/SOCKS4/SOCKS5  
✅ **Real-time Stats**: CPM, hits, errors  

## Architecture

```
Python GUI ←→ gRPC ←→ Go Engine
    ↓                      ↓
Stealth Layer       Fast HTTP Engine
(Playwright)        (Concurrent)
```

## Installation

### Prerequisites
- Go 1.21+
- Python 3.10+

### Setup

1. **Clone repository**
```bash
git clone https://github.com/basselshetifa-cloud/NewProj.git
cd NewProj
```

2. **Setup Go Engine**
```bash
cd go_engine
go mod download
protoc --go_out=. --go-grpc_out=. proto/checker.proto
go build -o checker_server
```

3. **Setup Python Client**
```bash
cd python_client
pip install -r requirements.txt
playwright install chromium
python -m grpc_tools.protoc -I../go_engine/proto --python_out=./proto --grpc_python_out=./proto ../go_engine/proto/checker.proto
```

## Usage

1. **Start Go Server**
```bash
cd go_engine
./checker_server
```

2. **Run Python GUI**
```bash
cd python_client
python gui.py
```

3. **Create Configs**
- Click "⚙️ CONFIG EDITOR" button
- Add blocks visually
- Save config as JSON
- Use in main checker

## Config Editor

The visual config editor uses OpenBullet-style blocks:

- 🟢 **REQUEST**: HTTP requests
- 🟡 **PARSE**: Extract data (JSON, Regex, CSS)
- 🔵 **KEY CHECK**: Validate results
- 🟢 **FUNCTION**: Hash, Base64, encryption
- 🟠 **UTILITY**: Helper functions

## Project Structure

```
📦 NewProj/
├── 📁 go_engine/              ← Go Backend (gRPC Server)
│   ├── main.go
│   ├── config_parser.go
│   ├── executor.go
│   ├── go.mod
│   └── proto/
│       └── checker.proto
├── 📁 python_client/          ← Python Frontend
│   ├── gui.py
│   ├── openbullet_editor.py
│   ├── stealth_checker.py
│   ├── grpc_client.py
│   └── requirements.txt
├── 📁 configs/                ← Config files
│   ├── steam.json
│   ├── discord.json
│   └── github.json
└── 📄 README.md
```

## License

MIT License
