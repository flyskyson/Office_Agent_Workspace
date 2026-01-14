# Chrome DevTools MCP 快速演示

## 🚀 启动步骤

### 方法 1: 使用演示脚本（推荐）

1. **双击运行**
   ```
   00_Agent_Library\99_Scripts_Tools\chrome_debug_demo.bat
   ```

2. **等待验证**
   - 脚本会自动关闭现有 Chrome
   - 以调试模式重新启动
   - 验证端口 9222 是否开启

3. **看到成功提示**
   ```
   ✓ Chrome 调试端口 9222 已开启！
   ```

### 方法 2: 手动启动

```powershell
# 在 PowerShell 中运行
# 1. 关闭 Chrome
Stop-Process -Name chrome -Force

# 2. 启动调试模式
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

---

## 🎯 演示命令

启动 Chrome 后，在 Claude Code 中尝试以下命令：

### 基础演示

```
1. "用 Chrome 访问 https://www.baidu.com"
2. "给我看看当前页面的快照"
3. "截取当前页面的截图"
```

### 高级演示

```
4. "查看页面的控制台消息"
5. "分析页面的网络请求"
6. "执行 JavaScript: document.title"
```

### 性能分析

```
7. "分析这个页面的性能"
8. "获取 Core Web Vitals 数据"
```

---

## 📊 验证清单

运行演示前，确认以下项目：

- [ ] Chrome 调试模式已启动（端口 9222）
- [ ] 在浏览器访问 http://localhost:9222 能看到 JSON
- [ ] 在 Claude Code 中输入 `/mcp` 能看到 `chrome-devtools`

---

## 🔧 故障排除

### 端口未开启
```bash
# 检查端口占用
netstat -ano | findstr :9222

# 如果被占用，关闭进程
taskkill /F /PID <进程ID>
```

### MCP 服务器未连接
1. 重新加载 VSCode 窗口
2. 检查 `.mcp.json` 配置
3. 确保 Chrome 以调试模式运行

---

## 📸 预期效果

成功后，您应该能够：

1. ✅ 通过 Claude Code 控制 Chrome
2. ✅ 自动导航、点击、输入
3. ✅ 实时查看页面快照
4. ✅ 获取控制台和网络信息
5. ✅ 执行性能分析

---

**文件位置**: `00_Agent_Library/CHROME_MCP_DEMO.md`
