# 聊天数据分析平台

实时读取聊天记录、自动脱敏、AI分析销冠话术、知识沉淀。

## 功能特性

### 核心功能
- 📊 **数据展示**：联系人列表、聊天记录查看、统计报表
- 🔍 **智能搜索**：全局搜索联系人、消息、FAQ
- 📈 **数据分析**：意图识别、成交信号检测、客户分群
- 📚 **知识库**：FAQ知识库管理、话术推荐

### 技术特性
- 🚀 **高性能**：基于FastAPI框架，响应速度快
- 🎨 **美观界面**：Bootstrap 5响应式设计
- 📱 **移动友好**：支持手机、平板访问
- 🔒 **安全可靠**：数据本地存储，隐私安全

## 快速开始

### 环境要求
- Python 3.8+
- 依赖包见 `requirements.txt`

### 安装步骤

1. **克隆项目**
```bash
cd wechat-ai-platform
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **准备数据**
确保以下数据文件存在：
- `F:\软件安装\WorkBuddy项目储存\2026-05-31-task-29\wechat-decrypt\export\contacts.json`
- `F:\软件安装\WorkBuddy项目储存\2026-05-31-task-29\wechat-decrypt\export\faq_knowledge_base.json`
- `F:\软件安装\WorkBuddy项目储存\2026-05-31-task-29\wechat-decrypt\export\statistics.json`

4. **启动服务**
```bash
python run.py
```

5. **访问应用**
- 首页：http://localhost:8000
- API文档：http://localhost:8000/api/docs
- 联系人：http://localhost:8000/contacts
- 聊天记录：http://localhost:8000/messages
- FAQ知识库：http://localhost:8000/faq
- 数据分析：http://localhost:8000/analysis

## 项目结构

```
wechat-ai-platform/
├── app/
│   ├── main.py              # FastAPI主程序
│   ├── api/                 # API接口
│   ├── models/              # 数据模型
│   ├── services/            # 业务逻辑
│   └── utils/               # 工具函数
├── static/
│   ├── css/                 # 样式文件
│   ├── js/                  # JavaScript文件
│   └── images/              # 图片资源
├── templates/               # HTML模板
├── data/                    # 数据文件
├── requirements.txt         # 依赖列表
├── run.py                   # 启动脚本
└── README.md                # 项目说明
```

## 数据来源

本项目基于现有数据：
- **联系人**：17,688人
- **消息**：327,917条
- **FAQ**：29,636个问答对
- **时间范围**：2021-2026年

## 适用场景

- 客服聊天记录分析
- 销售话术优化
- 知识库管理
- 数据可视化报表

## 注意事项

1. **数据安全**：聊天记录包含个人隐私，请妥善保管
2. **性能优化**：大量数据可能导致页面加载慢，建议分页显示
3. **浏览器兼容**：推荐使用Chrome、Firefox、Edge等现代浏览器

---

**版本**：v0.1.0  
**最后更新**：2026-06-13  
**状态**：开发中
