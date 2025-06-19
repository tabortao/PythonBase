
## 已经提交到云端，如何退回版本？

1、vscode 查看提交版本ID  如 3828d5b5d162469da4af4ce05b6a9bd8be2f1e15

2、彻底回退（丢弃后续提交的改动），注意备份好代码
```bash
git reset --hard 3828d5b5d162469da4af4ce05b6a9bd8be2f1e15
```

3、远程仓库需强制覆盖
```bash
git push origin main --force
```

