# i18n 资源提取与设计稿对照

仅在用户提供 i18n 资源、代码目录或要求从代码提取 UI 文案时加载本文件。提取用于审查和定位，不修改源资源、不生成翻译，也不推断资源对应的实际 UI 组件。

## 支持范围

脚本 `scripts/extract_i18n.py` 支持 `.json`、`.yaml`/`.yml`、Java `.properties` 静态资源：递归提取字符串叶节点，JSON/YAML 的嵌套对象扁平化为点分隔 key，数组项使用 `[索引]`；忽略非字符串值及 ARB 风格 `@key` 元数据。默认排除 `.git`、`node_modules`、`vendor`、`build`、`dist`、隐藏目录和缓存目录。暂不解析 JS/TS 模块、函数调用、JSONC 注释、运行时拼接、远程 CMS 或动态生成文案；不要把未提取项当成不存在。

YAML 需要可选依赖 PyYAML：`python3 -m pip install PyYAML`。JSON 保持严格 JSON；`.properties` 输出原始解码后文本，不展开 Java `\\uXXXX` 转义。ICU/插值占位符等运行时格式原样保留；脚本不尝试格式化或插值。

## 调用

从项目根目录提取并写 JSONL：

```bash
python3 scripts/extract_i18n.py ./src/locales \
  --root ./src/locales \
  --output /tmp/ui-copy.jsonl
```

强制指定 locale 并导出 CSV：

```bash
python3 scripts/extract_i18n.py ./locales/messages.json \
  --locale en-US --format csv --output /tmp/ui-copy.csv
```

也可传一个或多个文件/目录；支持 `--include-key REGEX`、`--exclude-key REGEX`。默认从路径段（如 `en-US`）推断 locale；推断不到时留空，绝不根据文案语言猜 locale。显式 `--locale` 覆盖路径推断。JSONL/CSV 每条包含 `key`、`locale`、`source_file`、`text`；`source_file` 是相对 `--root` 的路径（若无法相对则保留输入路径）。输出到 `-` 时写入 stdout。将导出文件放在代码库之外，避免将客户/产品文案误提交。

## 审查与设计稿关联

提取后，把记录中的 key、locale、source_file、text 与用户提供的设计稿/截图/文案映射表一并核对。保留原有字段及 key 作为定位依据；设计材料明确时补充页面、组件、状态，不明确时标为“未映射/待确认”，不要根据 key 名臆造按钮、错误提示或组件行为。筛选出当前设计实际使用的字符串，再按主 Skill 语言路由加载 HF 或明确指定的 en-US 规则；若同时给出源语言和目标语言，分别审查语言质量并对照语义。

输出问题时至少引用 `key`、资源文件、locale、原文、设计稿位置（如有）、规则 ID 和建议文案。只有用户要求时才生成 `COPY-` 清单。重复值、未被设计稿引用的 key、缺失 locale 对照、未映射 key 可以作为审计发现或待确认项，但不能自动断定为缺陷：代码引用关系、懒加载、实验开关、动态 key 与平台变体可能导致静态检索不完整。
