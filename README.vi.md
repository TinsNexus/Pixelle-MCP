<h1 align="center">Pixelle MCP - Khung Tri Tue Toan Mo Dang</h1>

<p align="center"><a href="README.md">English</a> | <a href="README_CN.md">Chinese</a> | <b>Tieng Viet</b></p>

<p align="center">Giai phap AIGC dua tren giao thuc MCP, ho tro ca ComfyUI cuc bo va ComfyUI cloud (RunningHub), chuyen doi workflow thanh cong cu MCP voi so code la khong.</p>

![](docs/readme-1.png)

https://github.com/user-attachments/assets/65422cef-96f9-44fe-a82b-6a124674c417

---

## Muc Luc

- [Tinh nang](#tinh-nang)
- [Kien truc du an](#kien-truc-du-an)
- [Bat dau nhanh](#bat-dau-nhanh)
- [Cai dat chi tiet](#cai-dat-chi-tiet)
- [Cau hinh](#cau-hinh)
- [Cau hinh MCP Server](#cau-hinh-mcp-server)
- [Su dung CLI](#su-dung-cli)
- [Trien khai Docker](#trien-khai-docker)
- [Tich hop voi CreatorHub](#tich-hop-voi-creatorhub)
- [Them cong cu MCP rieng](#them-cong-cu-mcp-rieng)
- [Quy tac workflow ComfyUI](#quy-tac-workflow-comfyui)
- [Xu ly su co](#xu-ly-su-co)
- [Cong dong](#cong-dong)
- [Dong gop](#dong-gop)
- [Loi cam on](#loi-cam-on)
- [Giay phep](#giay-phep)

---

## Tinh nang

- **Ho tro toan mo dang**: Ho tro chuyen doi va tao moi TISV (Van ban, Hinh anh, Am thanh, Video).
- **Che do thuc thi kep**: Moi truong ComfyUI tu hosting cuc bo + dich vu ComfyUI cloud RunningHub.
- **He sinh thai ComfyUI**: Xay dung tren [ComfyUI](https://github.com/comfyanonymous/ComfyUI), ke thua tat ca kha nang tu he sinh thai ComfyUI mo.
- **Phat trien khong can code**: Dinh nghia va trien khai giai phap Workflow-as-MCP Tool, ho tro them cong cu MCP moi dong thoi.
- **MCP Server**: Dua tren giao thuc [MCP](https://modelcontextprotocol.io/introduction), ho tro tich hop voi bat ky MCP client nao (Cursor, Claude Desktop, v.v.).
- **Giao dien Web**: Phat trien tren khung [Chainlit](https://github.com/Chainlit/chainlit), ho tro tuong tac da mo dang.
- **Trien khai mot nut**: Ho tro cai dat tu PyPI, lenh CLI, Docker va nhieu cach khac, san sang su dung ngay.
- **Cau hinh don gian**: Su dung phuong an cau hinh bien moi truong, don gian va truc quan.
- **Ho tro nhieu LLM**: Ho tro OpenAI, Ollama, Gemini, DeepSeek, Claude, Qwen va nhieu nua.

---

## Kien truc du an

Pixelle MCP su dung **kien truc thong nhat**, tich hop MCP server, giao dien web va dich vu file vao mot ung dung:

- **Giao dien web**: Giao dien tro chuyen dua tren Chainlit, ho tro tuong tac da mo dang
- **MCP Endpoint**: Cho cac MCP client ben ngoai (Cursor, Claude Desktop) ket noi
- **Dich vu file**: Xu ly tai len, tai xuong va luu tru file
- **Engine workflow**: Ho tro workflow ComfyUI cuc bo va cloud (RunningHub), tu dong chuyen doi workflow thanh cong cu MCP

![](docs/%20mcp_structure.png)

---

## Bat dau nhanh

### Phuong phap 1: Trai nghiem mot nut (uvx)

```bash
# Can cai dat uv truoc
# Khoi dong voi mot lenh, khong can cai dat vao he thong
uvx pixelle@latest
```

### Phuong phap 2: Cai dat pip

```bash
# Can Python 3.11
pip install -U pixelle
pixelle
```

### Phuong phap 3: Tu nguon

```bash
git clone https://github.com/AIDC-AI/Pixelle-MCP.git
cd Pixelle-MCP
uv run pixelle
```

Sau khi khoi dong, **huong dan cau hinh** se huong dan ban chon che do thuc thi va cau hinh LLM.

### Truy cap dich vu

- **Giao dien web**: http://localhost:9004 (ten dang nhau/mau khau mac dinh: `dev` / `dev`)
- **MCP Endpoint**: http://localhost:9004/pixelle/mcp

---

## Cai dat chi tiet

### Yeu cau

| Yeu cau | Chi tiet |
|---|---|
| Python | >= 3.11 |
| uv (de xuat) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| ComfyUI ( tuy chon ) | Chi can cho che do cuc bo. Xem [tai lieu ComfyUI](https://github.com/comfyanonymous/ComfyUI) |
| Tai khoan RunningHub ( tuy chon ) | Chi can cho che do cloud. Dang ky tai [runninghub.ai](https://www.runninghub.ai) |

### Cai dat qua uv (De xuat)

```bash
# Cai dat neu chua co
curl -LsSf https://astral.sh/uv/install.sh | sh

# Chay truc tiep khong can cai vao he thong
uvx pixelle@latest

# Hoac clone va chay tu nguon
git clone https://github.com/AIDC-AI/Pixelle-MCP.git
cd Pixelle-MCP
uv run pixelle
```

### Cai dat qua pip

```bash
# Dam bao Python 3.11 dang hoat dong
python3.11 -m pip install -U pixelle

# Khoi dong dich vu
pixelle
```

### Cai dat lan dau

Khi khoi dong lan dau, huong dan cau hinh se hoi ban:

1. **Chon engine thuc thi**: Chon ComfyUI cuc bo hoac dich vu cloud RunningHub
2. **Cau hinh LLM**: Thiet it mot nha cung cap LLM (API key + danh sach model)
3. **Tao cau truc thu muc**: He thong tu dong tao `data/custom_workflows/` va cac thu muc lien quan

---

## Cau hinh

### Bien moi truong

Copy `.env.example` thanh `.env` va chinh sua:

```bash
cp .env.example .env
```

#### Dich vu co ban

| Bien | Mac dinh | Mo ta |
|---|---|---|
| `HOST` | `localhost` | Dia chi rang buoc dich vu |
| `PORT` | `9004` | Cong dich vu |
| `PUBLIC_READ_URL` | `""` | URL truy cap cong khai (cho trien khai khong phai local) |

#### Tich hop ComfyUI (Che do cuc bo)

| Bien | Mac dinh | Mo ta |
|---|---|---|
| `COMFYUI_BASE_URL` | `http://localhost:8188` | Dia chi dich vu ComfyUI |
| `COMFYUI_API_KEY` | `""` | API key (can thiet neu dung API Nodes) |
| `COMFYUI_COOKIES` | `""` | Cookie xac thuc cho ComfyUI |
| `COMFYUI_EXECUTOR_TYPE` | `http` | Loai executor: `http` hoac `websocket` |

#### Che do cloud RunningHub

| Bien | Mac dinh | Mo ta |
|---|---|---|
| `RUNNINGHUB_BASE_URL` | `https://www.runninghub.ai` | URL API co so (dung `.cn` cho Trung Quoc) |
| `RUNNINGHUB_API_KEY` | `""` | API key RunningHub |

#### Nha cung cap LLM

| Bien | Mo ta |
|---|---|
| `OPENAI_BASE_URL` | URL API co so OpenAI |
| `OPENAI_API_KEY` | API key OpenAI ([lay tai day](https://platform.openai.com/api-keys)) |
| `CHAINLIT_CHAT_OPENAI_MODELS` | Danh sach model phay cach dau (vi du: `gpt-4o-mini`) |
| `OLLAMA_BASE_URL` | URL server Ollama cuc bo (mac dinh: `http://localhost:11434/v1`) |
| `OLLAMA_MODELS` | Danh sach model Ollama phay cach dau |
| `GEMINI_API_KEY` | API key Gemini ([lay tai day](https://aistudio.google.com/app/apikey)) |
| `GEMINI_MODELS` | Danh sach model Gemini phay cach dau |
| `DEEPSEEK_API_KEY` | API key DeepSeek ([lay tai day](https://platform.deepseek.com/api_keys)) |
| `DEEPSEEK_MODELS` | Danh sach model DeepSeek phay cach dau |
| `CLAUDE_API_KEY` | API key Anthropic ([lay tai day](https://console.anthropic.com/settings/keys)) |
| `CLAUDE_MODELS` | Danh sach model Claude phay cach dau |
| `QWEN_API_KEY` | API key Alibaba Cloud ([lay tai day](https://bailian.console.aliyun.com/)) |
| `QWEN_MODELS` | Danh sach model Qwen phay cach dau |
| `CHAINLIT_CHAT_DEFAULT_MODEL` | Model mac dinh cho cuoc tro chuyen |

#### Cai dat khac

| Bien | Mac dinh | Mo ta |
|---|---|---|
| `CHAINLIT_AUTH_SECRET` | `changeme-...` | Bi mat xac thuc (can doi o moi truong san xuat) |
| `CHAINLIT_AUTH_ENABLED` | `true` | Bat xac thuc |
| `CDN_STRATEGY` | `auto` | Che do CDN: `auto`, `china`, hoac `global` |

---

## Cau hinh MCP Server

### Dung nhu MCP Server doc lap

MCP endpoint nam tai:

```
http://localhost:9004/pixelle/mcp
```

### Cau hinh trong Cursor

Them vao file cau hinh MCP client (vi du: `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "pixelle": {
      "url": "http://localhost:9004/pixelle/mcp"
    }
  }
}
```

### Cau hinh trong Claude Desktop

Them vao `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pixelle": {
      "url": "http://localhost:9004/pixelle/mcp"
    }
  }
}
```

### Xac nhan ket noi

Sau khi ket noi, MCP client cua ban se phat hien cac cong cu (workflow) co san dong thoi. Moi workflow ComfyUI tu dong tro thanh mot cong cu MCP.

---

## Su dung CLI

### Lenh

| Lenh | Mo ta |
|---|---|
| `pixelle` | Vao che do tuong tac (mac dinh) |
| `pixelle start` | Khoi dong dich vu |
| `pixelle start -d` | Khoi dong o che do daemon (chay nen) |
| `pixelle start -f` | Khoi dong buoc (giet cac tien trinh trung khop) |
| `pixelle stop` | Dung tat ca tien trinh Pixelle |
| `pixelle status` | Hien trang thai dich vu |
| `pixelle logs` | Xem log gan day |
| `pixelle logs -f` | Theo doi log thuc te |
| `pixelle init` | Chay huong dan cau hinh |
| `pixelle edit` | Chinh sua cau hinh |
| `pixelle workflow` | Hien workflow da tai va cong cu MCP |
| `pixelle dev` | Hien thong tin phat trien/debug |

### Luong su dung pho bien

```bash
# Cai dat lan dau
pixelle init          # Cau hinh engine + LLM
pixelle start         # Khoi dong dich vu

# Su dung hang ngay
pixelle start -df     # Khoi dong buoc o nen
pixelle logs -f       # Giam sat log
pixelle stop          # Dung khi can

# Giai quyet van de
pixelle status        # Kiem tra tat ca
pixelle workflow      # Xac nhan cong cu da tai
pixelle dev           # Thong tin he thong day du
```

---

## Trien khai Docker

### Bat dau nhanh

```bash
git clone https://github.com/AIDC-AI/Pixelle-MCP.git
cd Pixelle-MCP

# Tao va chinh sua cau hinh
cp .env.example .env
# Chinh sua .env voi cai dat cua ban

# Khoi dong
docker compose up -d

# Xem log
docker compose logs -f
```

### Cau hinh Docker Compose

`docker-compose.yml` mac dinh mo cong `9004`, mount `./data` va `.env`, kem kiem tra suc khoe. Cac diem quan trong:

- Thu muc `data/` luu tru file workflow va cau hinh tuy chinh
- File `.env` duoc mount read-only vao container
- `host.docker.internal` duoc anh xa de truy cap ComfyUI cuc bo tu ben trong container
- Kiem tra suc khoe tai `http://localhost:9004/health`

### Lenh thuong dung

```bash
# Dung
docker compose down

# Xay dung lai sau khi thay doi ma nguon
docker compose build --no-cache && docker compose up -d

# Xem trang thai container
docker compose ps

# Vao shell container
docker compose exec pixelle bash
```

---

## Tich hop voi CreatorHub

Pixelle MCP co the tich hop vao CreatorHub (hoac bat ky he thong agent tuong thich MCP nao) nhu nha cung cap cong cu:

### 1. Dang ky nhu MCP Server

Dam bao Pixelle dang chay va truy cap duoc. MCP endpoint la:

```
http://localhost:9004/pixelle/mcp
```

### 2. Cau hinh CreatorHub

Trong cau hinh MCP server cua CreatorHub, them:

```json
{
  "pixelle": {
    "url": "http://localhost:9004/pixelle/mcp"
  }
}
```

### 3. Cong cu co san

Sau khi ket noi, CreatorHub se co quyen truy cap tat ca cong cu MCP duoc tao tu cac workflow ComfyUI cua ban. Moi workflow tro thanh mot cong cu co the goi voi tham so danh dau va mo ta.

### 4. Luong hoat dong

1. Thiet ke workflow trong ComfyUI
2. Xuat thanh file JSON API format
3. Tai len Pixelle qua giao dien web hoac dan vao cuoc tro chuyen
4. LLM tu dong chuyen doi workflow thanh cong cu MCP
5. CreatorHub co the goi cong cu qua giao thuc MCP

---

## Them cong cu MCP rieng

Mot workflow = Mot cong cu MCP. Hai cach de them:

- **Cach 1**: Workflow ComfyUI cuc bo - xuat file workflow API format
- **Cach 2**: Ma workflow RunningHub - dung ma workflow cloud truc tiep

### Cac buoc thuc hien

1. Xay dung workflow trong ComfyUI (vi du: lam mo hinh anh Gaussian)
2. Dat ten node voi cu phap DSL (xem [Quy tac workflow](#quy-tac-workflow-comfyui))
3. Xuat thanh file JSON **API format**
4. Mo giao dien web Pixelle va dan workflow JSON vao
5. LLM tu dong chuyen doi no thanh cong cu MCP
6. Lam moi trang - cong cu da san sang su dung

> **Nguoi dung RunningHub**: Ban chi can nhap ma workflow, khong can tai xuong va tai len file.

---

## Quy tac workflow ComfyUI

### Cu phap dinh nghia tham so

Trong ComfyUI, chinh sua ten node voi cu phap DSL nay:

```
$<ten_tham_so>.[~]<ten_truong>[!][:<mo_ta>]
```

| Ky hieu | Y nghia |
|---|---|
| `ten_tham_so` | Ten tham so cho ham cong cu MCP |
| `~` | (Tuy chon) Xu ly tai len URL, tra ve duong dan tuong doi |
| `ten_truong` | Truong input tuong ung trong node |
| `!` | Dau hieu tham so bat buoc |
| `mo_ta` | Mo ta tham so |

### Vi du

**Tham so bat buoc:**
- Ten node: `$image.image!:Nhap URL hinh anh`
- Tao tham so bat buoc `image` tuong ung voi truong `image` cua node

**Xu ly tai len URL:**
- Ten node: `$image.~image!:Nhap URL hinh anh`
- He thong tu dong tai URL va tai len ComfyUI

### Suy luan kieu du lieu

He thong suy luan kieu tu gia tri hien tai cua node:
- `int` - gia tri nguyen (512, 1024)
- `float` - so thuc (1.5, 3.14)
- `bool` - boolean (true, false)
- `str` - chuoi (mac dinh)

### Dinh nghia dau ra

**Node tu dong nhan biet**: `SaveImage`, `SaveVideo`, `SaveAudio`, `VHS_SaveVideo`, `VHS_SaveAudio`

**Danh dau dau ra thu cong** (cho nhieu dau ra):
- Ten node: `$output.result`

### Mo ta cong cu (Tuy chon)

Them node `String (Multiline)` voi ten `MCP` va nhap mo ta cong cu trong truong gia tri.

### Luu y quan trong

1. Tham so tuy chon (khong co `!`) phai co gia tri mac dinh trong node
2. Cac truong da ket noi voi node khac se khong duoc phan tach thanh tham so
3. Ten file xuat se la ten cong cu - su dung ten tieng Anh co y nghia
4. Phai xuat duoi dang **API format**, khong phai UI format
5. Kiem tra workflow trong ComfyUI truoc khi them vao Pixelle

---

## Xu ly su co

### Dich vu khong khoi dong duoc

```bash
pixelle status       # Kiem tra trang thai
pixelle start -f     # Khoi dong buoc
pixelle logs         # Kiem tra log loi
```

### Cong da bi chiem

```bash
# Doi cong trong .env
PORT=9005

# Hoac khoi dong buoc de giet tien trinh trung khop
pixelle start -f
```

### Ket noi ComfyUI that bai

1. Dam bao ComfyUI dang chay: `curl http://localhost:8188/system_stats`
2. Kiem tra `COMFYUI_BASE_URL` trong `.env`
3. Khi dung Docker, dam bao `host.docker.internal` truy cap duoc

### Ket noi RunningHub that bai

1. Xac nhan API key tai [runninghub.ai](https://www.runninghub.ai)
2. Kiem tra `RUNNINGHUB_BASE_URL` (dung `.cn` cho Trung Quoc)
3. Dam bao truy cap mang den may chu RunningHub

### LLM khong phan hoi

1. Dam bao API key da duoc thiet lap trong `.env`
2. Kiem tra `CHAINLIT_CHAT_DEFAULT_MODEL` da duoc cau hinh
3. Kiem tra API key doc lap:
   ```bash
   # Kiem tra OpenAI
   curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

### Van de Docker

```bash
docker compose down && docker compose build --no-cache && docker compose up -d
docker compose logs -f
```

### Dat lai cau hinh

```bash
pixelle init    # Chay lai huong dan cau hinh
```

---

## Cong dong

| Discord | WeChat |
|:---:|:---:|
| <img src="docs/discord.png" alt="Discord" width="200" /> | <img src="docs/wechat.png" alt="WeChat" width="200" /> |

---

## Dong gop

Chung toi don nhan moi hinh thuc dong gop!

### Bao cao loi
- Gui bao cao loi tai [Issues](https://github.com/AIDC-AI/Pixelle-MCP/issues)
- Tim kiem cac van de tuong tu truoc khi gui
- Mo ta chi tiet cac buoc tai tao va moi truong

### De xuat tinh nang
- Gui yeu cau tinh nang tai [Issues](https://github.com/AIDC-AI/Pixelle-MCP/issues)
- Mo ta truong hop su dung va cach cai thien trai nghiem

### Dong gop ma nguon

1. Fork kho nay
2. Tao nhan tinh nang: `git checkout -b feature/your-feature-name`
3. Phat trien va them kiem thu
4. Commit: `git commit -m "feat: add your feature"`
5. Push: `git push origin feature/your-feature-name`
6. Tao Pull Request

### Phong cach ma nguon
- Ma Python theo [PEP 8](https://pep8.org/)
- Them tai lieu va ghi chu cho cac tinh nang moi

### Dong gop workflow
- Chia se workflow ComfyUI cua ban voi cong dong
- Gui cac file workflow da kiem thu voi huong dan su dung

---

## Loi cam on

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Chainlit](https://github.com/Chainlit/chainlit)
- [MCP](https://modelcontextprotocol.io/introduction)
- [WanVideo](https://github.com/Wan-Video/Wan2.1)
- [Flux](https://github.com/black-forest-labs/flux)
- [LiteLLM](https://github.com/BerriAI/litellm)

## Giay phep

Du an nay duoc phat hanh duoi giay phep MIT ([LICENSE](LICENSE), SPDX-License-identifier: MIT).

## Lich su Star

[![Star History Chart](https://api.star-history.com/svg?repos=AIDC-AI/Pixelle-MCP&type=Date)](https://star-history.com/#AIDC-AI/Pixelle-MCP&Date)
