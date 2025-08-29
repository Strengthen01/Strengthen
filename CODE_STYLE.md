# CODE_STYLE

- 命名：变量/函数使用 snake_case，类使用 CamelCase。
- 注释：中文注释，每句不超过 80 字符；模块/类/函数必须写 docstring。
- 结构：每个模块职责单一；公共常量放在模块顶部。
- 质量检查：使用 flake8（见 requirements-dev.txt）。
- 日志：统一使用 logging 模块；文件输出到 logs/traffic_control.log。
