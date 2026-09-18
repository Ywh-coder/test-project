# api-test-project

接口自动化测试项目，基于 pytest + requests 框架，针对 [RESTful Booker](https://restful-booker.herokuapp.com) 公开 API 进行接口测试。

## 技术栈

- Python 3.8+
- pytest
- requests
- pytest-html（生成 HTML 测试报告）
- allure-pytest（生成 Allure 测试报告）

## 目录结构

`
api-test-project/
├── common/              # 公共方法
│   ├── __init__.py
│   ├── request_util.py  # 封装 requests
│   └── logger.py        # 日志
├── testcases/           # 测试用例
│   ├── __init__.py
│   ├── conftest.py      # pytest 夹具
│   ├── test_auth.py     # 登录相关
│   └── test_booking.py  # 预订相关
├── data/                # 测试数据
│   └── booking_data.json
├── report/              # 测试报告输出
├── pytest.ini           # pytest 配置
├── requirements.txt
└── README.md
`

## 安装依赖

`ash
pip install -r requirements.txt
`

## 运行测试

### 基础运行

`ash
pytest
`

### 带 HTML 报告

`ash
pytest --html=report/report.html --self-contained-html
`

运行完成后用浏览器打开 eport/report.html 查看报告。

### 生成 Allure 报告（进阶）

`ash
pytest --alluredir=report/allure-results
allure serve report/allure-results
`

## 测试用例覆盖

| 模块 | 用例 | 说明 |
|------|------|------|
| Auth | test_login_success | 正常登录 |
| Auth | test_login_wrong_password | 错误密码 |
| Auth | test_login_empty_params | 空账号/密码（参数化） |
| Booking | test_get_booking_ids | 查询所有预订 |
| Booking | test_create_booking | 创建预订 |
| Booking | test_get_booking_detail | 查询预订详情 |
| Booking | test_update_booking | 更新预订（PUT） |
| Booking | test_delete_booking | 删除预订 |
| Booking | test_get_nonexistent_booking | 查询不存在的预订 |
