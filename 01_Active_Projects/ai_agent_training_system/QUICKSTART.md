# AI Agent Training System - 快速开始指南

## 🚀 5分钟快速启动

### 步骤1: 安装依赖

```bash
cd 01_Active_Projects/ai_agent_training_system
pip install -r requirements.txt
playwright install chromium
```

### 步骤2: 启动测试网站

```bash
# 方式1: 使用批处理文件（Windows）
start_test_site.bat

# 方式2: 直接运行
python test_site/server.py
```

访问: http://127.0.0.1:5555

测试账号: `test_user` / `test123`

### 步骤3: 启动AI培训老师

```bash
# 方式1: 使用批处理文件（Windows）
start_ai_tutor.bat

# 方式2: 直接运行
streamlit run ai_tutor_bot/app.py
```

访问: http://localhost:8501

### 步骤4: 测试自动化

```bash
python test_automation.py
```

---

## 📁 项目结构

```
ai_agent_training_system/
├── automation_agents/         # 多Agent自动化系统
│   └── supervisor.py          # 监督者Agent（核心）
│
├── ai_tutor_bot/             # AI培训老师
│   └── app.py                # Streamlit应用
│
├── test_site/                # 测试网站
│   ├── server.py             # Flask服务器
│   └── templates/            # HTML模板
│
├── test_automation.py        # 自动化测试脚本
├── start_test_site.bat       # 启动测试网站
├── start_ai_tutor.bat        # 启动AI培训老师
└── requirements.txt          # 依赖包
```

---

## 🎯 学习路径

### Week 1: 基础入门
- Day 1-2: Playwright基础
- Day 3: Streamlit入门
- Day 4-5: 登录和表单自动化
- Day 6-7: 综合练习和总结

### Week 2: 核心技术
- Day 8-10: LangGraph和Agent设计
- Day 11-14: 多Agent开发和集成

### Week 3: 高级集成
- Day 15-17: MCP工具和优化
- Day 18-21: 部署和项目总结

---

## 🧪 测试说明

### 测试完整工作流
```bash
python test_automation.py
# 选择: 1. 测试完整工作流
```

### 单独测试Agent
```bash
python test_automation.py
# 选择: 2. 单独测试各个Agent
```

---

## 📚 重要文件说明

| 文件 | 说明 |
|------|------|
| [supervisor.py](automation_agents/supervisor.py) | 多Agent监督者，协调所有Agent工作 |
| [app.py](ai_tutor_bot/app.py) | AI培训老师界面，提供学习路径 |
| [server.py](test_site/server.py) | 测试网站，模拟真实办事平台 |
| [test_automation.py](test_automation.py) | 自动化测试脚本 |

---

## ✅ 成功标准

完成学习后，你应该能够：

- [ ] 理解并使用Playwright进行浏览器自动化
- [ ] 掌握LangGraph工作流设计
- [ ] 能够设计并实现多Agent系统
- [ ] 能独立开发类似的自动化Agent
- [ ] 理解并能修改核心代码

---

## 🆘 常见问题

### Q: Playwright浏览器未安装？
A: 运行 `playwright install chromium`

### Q: 端口被占用？
A: 修改 `test_site/server.py` 中的端口号

### Q: 测试失败？
A: 确保测试网站正在运行（http://127.0.0.1:5555）

---

## 📞 获取帮助

- 查看项目文档: [README.md](README.md)
- 查看工作区文档: [../../docs/](../../docs/)
- 查看学习路径: 启动AI培训老师应用

---

**祝你学习愉快！** 🎓
