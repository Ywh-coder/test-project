# api-test-project

接口自动化测试项目，基于 pytest + requests 框架，针对 [RESTful Booker](https://restful-booker.herokuapp.com) 公开 API 进行接口测试。

## 技术栈

- Python 3.8+
- pytest
- requests
- pytest-html（生成 HTML 测试报告）
- allure-pytest（生成 Allure 测试报告）
- > 需要先安装 Allure 命令行工具：https://docs.qameta.io/allure/#_installing_a_commandline

## 目录结构

```text
api-test-project/
├── common/              # 公共方法
│   ├── __init__.py
│   ├── request_util.py  # 封装 requests
│   ├── logger.py        # 日志
│   └── data_loader.py   # JSON 数据加载
├── testcases/           # 测试用例
│   ├── __init__.py
│   ├── conftest.py      # pytest 夹具
│   ├── test_auth.py     # 登录相关
│   ├── test_booking.py  # 预订相关（正常用例）
│   └── test_booking_invalid.py  # 预订异常用例
├── data/                # 测试数据（JSON 数据驱动）
│   └── booking_data.json
├── report/              # 测试报告输出（已加入 .gitignore）
├── pytest.ini           # pytest 配置
├── requirements.txt
└── README.md
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

### 基础运行

```bash
pytest
```

### 带 HTML 报告

```bash
pytest --html=report/report.html --self-contained-html
```

运行完成后用浏览器打开 
report/report.html 查看报告。

### 生成 Allure 报告（进阶）

```bash
pytest --alluredir=report/allure-results
allure serve report/allure-results
```

### 按标记运行

```bash
# 只跑冒烟测试
pytest -m smoke

# 只跑回归测试
pytest -m regression
```

## 测试结果

当前 **17 个用例16个通过,还有1 xfailed**，覆盖认证 + 预订 CRUD + 异常场景：

| 模块 | 用例数 | 说明 |
|------|-----|------|
| Auth | 5   | 正常登录 / 错误密码 / 空参数（3 组） |
| Booking（正常） | 7   | 查询列表 / 创建（2 组参数化） / 详情 / 更新 / 删除 / 404 |
| Booking（异常） | 5   | 缺字段 / 负数价格 / 字符串价格 / 无 token 更新 / 删除不存在的预订 |

## 测试用例覆盖

### 认证模块（test_auth.py）

| 用例 | 说明 | 标记 |
|------|------|------|
| test_login_success | 正确账号密码登录成功，返回 token | smoke |
| test_login_wrong_password | 密码错误，返回 Bad credentials | regression |
| test_login_empty_params (3组) | 空用户名 / 空密码 / 全空 | regression |

### 预订模块 - 正常流程（test_booking.py）

| 用例 | 说明 | 标记 |
|------|------|------|
| test_get_booking_ids | 查询所有预订，列表非空 | smoke |
| test_create_booking (2组) | 创建预订（无押金 / 有押金） | smoke |
| test_get_booking_detail | 通过 booking_id 查询详情 | regression |
| test_update_booking | PUT 更新预订信息 | regression |
| test_delete_booking | DELETE 删除预订，返回 201 | regression |
| test_get_nonexistent_booking | 查询不存在 ID，返回 404 | regression |

### 预订模块 - 异常流程（test_booking_invalid.py）

| 用例 | 说明 | 标记 |
|------|------|------|
| test_create_booking_invalid_fields (3组) | 缺字段→期望400(实际500, xfail) / 负数价格→200 / 字符串价格→200 | regression |
| test_update_without_auth_token | 不带 token 更新，期望 403 | regression |
| test_delete_nonexistent_booking | 删除不存在预订，期望 405 | regression |

## 设计说明

- **数据驱动**：所有测试数据统一存放在 data/booking_data.json，通过 load_data() 加载，避免硬编码
- **夹具设计**：uth_token（session 级）登录一次获取全局 token；create_booking（函数级）自动创建并清理数据，teardown 容忍 405/404（booking 已被用例删除的情况）
- **日志截断**：请求参数和响应体均做长度限制，防止大文件导致日志爆炸
- **异常容错**：teardown 清理时 405/404 视为已清理，仅非预期状态才打 warning
