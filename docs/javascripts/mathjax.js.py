// noinspection JSUnresolvedVariable,JSUnusedGlobalSymbols

window.MathJax = {
  tex: {
    // This enables the $ symbol for inline math
    inlineMath: [["$", "$"], ["\\(", "\\)"]],
    displayMath: [["$$", "$$"], ["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmateia"
  }
};

/* eslint-disable */
// Wait for MkDocs Material to load the page
if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    // Re-render math when navigating to a new page (Instant Loading)
    MathJax.typesetPromise();
  });
}