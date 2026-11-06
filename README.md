# 粤菜功能知识库

按关键词搜索粤菜需求的标题、解决内容、编号及分类，查看对应的本地 PDF。

当前收录 **77 条记录、80 份 PDF**，另附需求问题总结 Excel。PDF 和索引都随 Skill 一起下载，安装后可离线使用，不需要钉钉账号或网页服务。

## 在 Codex 中安装

把下面这句话发给 Codex：

> 使用 $skill-installer 安装 https://github.com/liuhuancheng719/lhc/tree/main/skills/yuecai-knowledge-search

安装完成后，在后续消息中使用：

> 使用 $yuecai-knowledge-search 搜索“拆席”，打开对应 PDF。

也可以搜索“计件提成”“做法分摊”或需求编号。首次执行脚本需要本机有 Python 3；脚本没有第三方依赖。未显示新技能时重启 Codex 后再试。

## 下载后直接使用

通过仓库的 **Code → Download ZIP** 下载并解压后，打开：

`skills/yuecai-knowledge-search/assets/library/打开目录.html`

页面支持离线搜索和点击查看 PDF。PDF 文件夹需要保留在原位置。GitHub 的文件预览不会运行 HTML 搜索页面。

## 项目结构

```text
skills/yuecai-knowledge-search/
├── SKILL.md
├── agents/openai.yaml
├── scripts/search.py
└── assets/library/
    ├── catalog.json
    ├── 打开目录.html
    ├── progressive-reveal.css
    ├── progressive-reveal.js
    ├── PDF/
    ├── 粤菜需求_问题总结.xlsx
    ├── 文档导出清单.json
    └── 使用说明.txt
```

## 更新资料

维护者核对好资料包后，在项目根目录执行：

```bash
python3 scripts/sync_library.py --source "/资料包的实际路径"
python3 -m unittest discover -s tests
```

同步脚本只复制知识库页面、PDF、索引、总结表和说明，不复制缓存、下载凭证或个人配置。随后提交并推送 GitHub；如果记录数量变化，同步修改本说明中的数量。

使用者已安装的 Skill 是本地副本，不会随 GitHub 自动更新。可让 Codex 获取最新版本并更新已安装目录；普通首次安装命令遇到同名已安装目录会停止，不能将再次安装视为自动覆盖。通过 Git 克隆项目且直接使用该目录的用户可以 `git pull`，但单独复制出去的 Skill 仍需同步更新。

## 内容范围

搜索默认使用索引中的标题、简介、编号和分类，不是全文检索。没有记录的需求编号留空。部分 PDF 是原文直接导出，部分由原始 Word 的正文、表格和内嵌图片转换，重新分页；具体方式见文档导出清单。
