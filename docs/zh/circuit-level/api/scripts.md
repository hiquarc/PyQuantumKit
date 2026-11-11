# 翻译脚本参考
本文列出PyQuantumKit内置支持的量子开发框架和量子编程语言的翻译脚本，供用户自己编写翻译脚本时参考。

## 基于Python的量子开发框架
### qiskit
```python title="qiskit.py"
--8<-- "pyquantumkit/translate/translate_scripts/qiskit.py"
```

### pyqpanda3
```python title="pyqpanda3.py"
--8<-- "pyquantumkit/translate/translate_scripts/pyqpanda3.py"
```

### pyquafu
注：这里的pyquafu对应的是**旧版PyQuafu平台**，文档网址：[https://scq-cloud.github.io/](https://scq-cloud.github.io/)

2026年10月Quafu平台进行了一次更新，不再使用旧版pyquafu提交量子线路，而是使用OpenQASM 2.0语法提交量子线路。详见新版Quafu平台网址：[https://quafu.com.cn/](https://quafu.com.cn/)

```python title="pyquafu.py"
--8<-- "pyquantumkit/translate/translate_scripts/pyquafu.py"
```

### cqlib
```python title="cqlib.py"
--8<-- "pyquantumkit/translate/translate_scripts/cqlib.py"
```

## 其他量子编程语言
### OpenQASM 2.0

### Q\#
```python title="qsharp.py"
--8<-- "pyquantumkit/translate/extra/qsharp.py"
```

### isQ
```python title="isq.py"
--8<-- "pyquantumkit/translate/extra/isq.py"
```
