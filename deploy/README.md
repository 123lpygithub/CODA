# CODA 可选远程部署方案

源码用户的默认方式是本地安装、单地址运行，见 [项目 README](../README.md)。下面仅适用于另有远程访问需求的部署。

本方案针对当前 React + Vite 前端、FastAPI 后端和本地文件检查点实现。研究日期：2026-11-04。

**需要独立托管前端时推荐：使用 Cloudflare Pages 的 Git 集成。** 前端体积约 550 KB，不需要 Node 常驻进程；Pages 提供静态托管、HTTPS、预览和回滚，GitHub 推送后自动构建。后端继续运行在有持久化磁盘的机器上，浏览器直接访问它的 HTTPS API。

如果还没有可访问的后端，先上线 Pages 只能得到界面。要让别人完成整个分析，必须同时提供后端连接。现有后端包含长时间的模型请求、API Key 和 `runs/` 检查点，不能一起上传成静态文件，也不适合直接搬进短时 serverless 函数。

## 一、方案比较

| 方案 | 免费部分与维护方式 | 适合 CODA 的程度 |
| --- | --- | --- |
| **Cloudflare Pages + GitHub** | 免费静态托管、HTTPS；主分支自动部署，其他分支可生成预览；Free 每月 500 次构建 | **前端首选。** 保留 Python 后端，通过公开 HTTPS 地址或研究者的私有网络访问 |
| Vercel Hobby | 免费个人项目，Git 自动部署；官方限制为个人、非商业用途 | 也能部署 Vite，但 CODA 不需要其全栈功能；组织使用需先核对计划范围 |
| Netlify Free | Git 部署；当前免费计划每月 300 credits，多类资源共用额度 | 可用，但部署、流量等计费项需要一起关注，预算较难直观判断 |
| GitHub Pages | 静态站点、Actions 自动部署 | 可用，但项目子路径需设置 Vite base；私有仓库与组织权限取决于 GitHub 计划 |
| **已有服务器 + Caddy** | Caddy、HTTPS 证书免费；计算机/域名/网络由自己提供 | **完整系统最直接。** 同域提供前后端，可在入口统一设置密码；维护成本高于纯静态 Pages |

Pages 的免费额度不包含模型调用费用，也不提供当前 Python 后端的持久化计算服务。不要为了“全免费”把长任务放到会休眠且磁盘不持久的临时实例中。

## 二、当前项目已补齐的部署配置

1. `frontend/src/api.ts`：开发默认连接 `http://127.0.0.1:8003`；生产默认同域 `/api`，或使用构建变量 `VITE_API_BASE_URL` 指定 HTTPS 后端。地址末尾 `/` 自动去除。
2. `frontend/vite.config.ts`：生产构建拒绝 HTTP、localhost、凭据、查询参数或带路径的 API 地址，避免上线后仍请求访问者自己的电脑。未设置或空字符串表示同域代理。
3. `frontend/public/_headers`：Pages 静态安全头；带哈希的 `/assets/*` 长缓存，入口 HTML 重新验证，避免发布后长期停留在旧页面。Vite 会自动复制到 `dist/`。
4. `CODA_ALLOWED_ORIGINS`：后端支持逗号分隔的精确前端 origin，本地开发仍可用。拒绝 `*` 和包含路径的值。
5. `deploy/Caddyfile`：同一服务器部署前后端的可选示例，保留 `/api` 前缀，入口使用密码，前端使用 SPA fallback。

`VITE_API_BASE_URL` 是公开配置。所有 `VITE_*` 变量都会进入浏览器构建产物，**不能填写 RightAPI、OpenAI 或其他模型 API Key**。

## 三、Pages 首次部署步骤

### 1. 先确定后端地址

下面以 `https://api.example.org` 为占位示例，必须替换为真实可访问的后端。浏览器请求路径最终是 `https://api.example.org/api/...`，所以变量不要带 `/api`。

后端可以是已有服务器，或在私有 VPN/研究网络内运行、但对使用者可达的 HTTPS 地址。仅有 `http://127.0.0.1:8003` 不足以供远程浏览器访问。HTTPS 前端也不应直接访问普通 HTTP 后端。

**当前 API 尚未实现多用户鉴权和研究者之间的数据隔离。** 跨域白名单不是登录验证。私人研究使用应通过 VPN/已有受保护入口访问后端；不能把能够创建、删除运行并调用付费模型的 API 无保护地开放给所有人。若计划让不在私有网络里的多位用户直接在线操作，使用下一节的同域、统一入口部署更省事，或后续实现用户登录与授权。

### 2. 在 Cloudflare Pages 创建项目

在 Cloudflare 控制台进入 Pages 的创建应用入口，连接 GitHub，选择 `linli1724647576/FSE27-CODA`。不同版本控制台的菜单名称可能变化，关键是选择 **Pages + Git repository**，不是创建短时 Worker 来运行 Python。

| 设置 | 填写值 |
| --- | --- |
| 生产分支 | `main` |
| 根目录 / Root directory | `CODA/frontend` |
| 框架预设 | Vite / React，或 None 后手动填写下面两项 |
| Build command | `npm ci && npm run build` |
| Build output directory | `dist`（相对于 frontend） |
| `NODE_VERSION` | `22`，至少 22.12；以当前 Vite 依赖要求为准 |
| `VITE_API_BASE_URL` | 真实后端 origin，例如 `https://api.example.org` |

Pages 通常会自动安装依赖；这里显式 `npm ci` 是为了按 `package-lock.json` 固定依赖。若开启了平台自动安装，会多做一次安装；也可按平台当前设置关闭自动安装后保留上述构建命令。

首次使用平台提供的 `https://<项目名>.pages.dev` 即可，不需要购买域名。只有部署准备文件会上传，`runs/`、模型密钥和原始研究文件不会因为 Pages 构建而进入静态站点。

### 3. 后端允许这个前端来源

在启动后端的终端或服务配置中设置：

```bash
export CODA_ALLOWED_ORIGINS='https://coda-workbench.pages.dev'
# 同时保留原有模型供应商配置和 API Key，不要把它们设置到 Pages。
python scripts/run_web_api.py --host 127.0.0.1 --port 8003 --runs-root runs/web
```

`coda-workbench.pages.dev` 是示例，必须使用 Pages 实际分配的站点地址。前面需要有 HTTPS 入口或使用者能访问的私有 HTTPS 网络地址，反向代理到 `127.0.0.1:8003`。`127.0.0.1` 用于服务器内部监听，不能作为 Pages 的后端地址。

多个正式地址用逗号分隔，例如：

```bash
export CODA_ALLOWED_ORIGINS='https://coda-workbench.pages.dev,https://coda.example.org'
```

预览分支有自己的来源。需要连接后端时，显式加入相应预览 origin 或给预览使用独立测试后端，不要为了方便将所有来源开放。

### 4. 验证

- 在最终访问网络中打开前端，确认加载数据集和保存运行。
- 浏览器 Network 中请求应发往配置的 HTTPS 后端，不能是 `127.0.0.1`，也不能出现 `/api/api/`。
- `GET https://api.example.org/api/health` 应返回 `{"status":"ok"}`；若后端受私有网络或入口访问保护，使用相应网络/登录方式检查。
- 用测试运行检查 Initial / Triggered / Final Review 和停止恢复，不要先跑正式全量实验。
- 首次验证长任务要持续超过两分钟，以确认 HTTPS 入口不会提前截断请求。

生产构建变量在构建时固定：改变 `VITE_API_BASE_URL` 后要重新部署，不是只重启后端。

## 四、最容易被忽视的问题：长请求代理超时

当前 `POST /initialize`、`POST /prepare-review`、`POST /process-automatic` 等接口会等待实际模型工作结束才返回。有些持续数分钟；浏览器同时轮询进度，但主请求仍然保持打开。

Cloudflare 官方当前文档给出的默认 Proxy Read Timeout 是 **125 秒**。因此，不能把 API 不加改造地放在橙云代理、Pages Functions 或 Cloudflare Tunnel 后，就认为所有工作流都能稳定执行。前端静态文件放 Pages 没问题，问题是 **API 的长连接经过哪一层**。只改 CORS 或前端 API 地址不能解决它。

现在有两个可行选择：

1. **最少改动：** Pages 托管前端，浏览器直接访问已有、可持续响应长请求的 HTTPS 后端入口。若在 Cloudflare 管理 DNS，API 子域名可用 DNS-only，HTTPS 由服务器上的 Caddy/Nginx 提供；后端入口仍需私有网络或适当鉴权。
2. **后续做成正式在线服务：** 将长操作改成提交后立即返回 `job_id`，前端轮询进度和结果，停止接口取消 job。模型执行和检查点留在持久化 worker。这样才能可靠经过短请求代理，也方便重连和多人使用。这比单独上线前端需要更多后端改动，当前没有冒称已实现。

不要把前端自动重发长 POST 当作解决办法，这可能重复提交操作。后端无限重试模型超时与代理截断浏览器连接是两种问题。

## 五、没有独立 API 域名时：同一服务器部署最省事

如果已有一台长期运行、能接收 HTTPS 访问的机器，可直接用 Caddy 在同域提供静态页面和 API。它同时解决 HTTPS、跨域、入口密码和长请求转发；无需额外静态托管账号。它的软件免费，机器和域名是否产生费用取决于已有资源。

1. 为机器配置域名 DNS 和 80/443 入站访问。后端仍只监听 `127.0.0.1:8003`。
2. 在项目根目录构建，生产 API 采用同域：

   ```bash
   VITE_API_BASE_URL='' npm --prefix frontend ci
   VITE_API_BASE_URL='' npm --prefix frontend run build
   # 按实际服务器权限把 frontend/dist/ 部署到 /srv/coda/frontend/
   ```

3. 安装 Caddy，使用 `deploy/Caddyfile`，配置 `CODA_SITE_DOMAIN`、`CODA_SITE_USER`、`CODA_SITE_PASSWORD_HASH`。密码哈希用 `caddy hash-password` 交互生成，存入服务环境文件，不提交 Git。
4. 用 `caddy validate --config deploy/Caddyfile --adapter caddyfile` 检查配置，再由 systemd 或现有服务管理器启动 Caddy 和 Python 后端。环境变量应在相应服务进程中配置。
5. 先登录入口密码，再打开工作台。同域 API 自动携带浏览器入口认证；模型密钥只保存在 Python 后端。
6. 更新时 `git pull`、`npm ci`、`npm run build`，再发布 `dist`；后端有变更时重启 Python 服务。正式运行应采用版本目录切换/保留上一版以便回退，并持续备份 `runs/`。

此方案的入口密码只是保护共享工作台，不会让研究者的数据相互隔离。不要把它描述为多租户系统。

## 六、后续维护

- 前端修改提交并推送 `main` → Pages 自动构建和上线；失败构建不会替换现有成功部署。
- 工作分支可用于预览；预览默认不应访问正式研究运行。
- 前端静态部署不会自动更新 Python 服务；后端协议变更应协调发布。
- 使用平台部署历史回滚前端；后端持久化数据另外备份。
- 可用 build watch paths 只监听 `frontend/**` 来减少无关提交触发构建；同时考虑平台配置文件变化。
- 当前还通过 Google Fonts 加载字体。需要在受限网络中稳定展示时可将所需字体自托管，再做许可/体积检查；它不影响 API 部署方式。

## 七、核实过的官方资料

下面链接于研究时成功读取；额度与限制以后可能变化，以部署时控制台和官方文档为准。

- [Cloudflare Pages 免费计划限制：构建次数、文件数量和大小](https://developers.cloudflare.com/pages/platform/limits/)
- [Pages Git 集成与自动部署](https://developers.cloudflare.com/pages/configuration/git-integration/)
- [Pages 静态服务与 SPA fallback](https://developers.cloudflare.com/pages/configuration/serving-pages/)
- [Pages `_headers` 配置](https://developers.cloudflare.com/pages/configuration/headers/)
- [Cloudflare 524 与默认代理读超时](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-524/)
- [Vercel Hobby 使用范围](https://vercel.com/docs/plans/hobby)
- [Netlify 当前计划与 credits](https://www.netlify.com/pricing/)
- [Vite 环境变量：构建时公开 `VITE_*`](https://vite.dev/guide/env-and-mode)

当前没有替用户创建云账号、绑定 GitHub 或发布到外部平台。代码中的部署准备可以本地审查；实际建站时按第三节填写即可。
