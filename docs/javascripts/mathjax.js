window.MathJax = {
  tex: {
    packages: {'[+]': ['ams', 'amsmath', 'autoload']},
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true
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
