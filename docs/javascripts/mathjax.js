window.MathJax = {
  tex: {
    packages: {'[+]': ['ams', 'amsmath', 'autoload']},
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
    macros: {
      bra: ['\\langle #1 |', 1],
      ket: ['| #1 \\rangle', 1],
      braket: ['\\langle #1 \\rangle', 1],
      set: ['\\{ #1 \\}', 1],
      // 自动调整大小的版本（等价于 \left \right）
      Bra: ['\\left\\langle #1 \\right|', 1],
      Ket: ['\\left| #1 \\right\\rangle', 1],
      Braket: ['\\left\\langle #1 \\right\\rangle', 1],
      Set: ['\\left\\{ #1 \\right\\}', 1]
    }
  },
  options: {
    processHtmlClass: "arithmatex",
  },
};

document$.subscribe(() => {
  if (typeof MathJax !== 'undefined') {
    MathJax.typesetPromise().catch((err) => {
      console.error('MathJax typesetting error:', err);
    });
  }
});
