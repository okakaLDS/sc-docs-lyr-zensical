/* =============================================================================
   Zensical版専用スクリプト（正本の javascripts/extra.js の後に読み込む）
   document$ はインスタントナビゲーションでページが切り替わるたびに発火する。
   ============================================================================= */

/* サイトはSampleだけを載せるので、ナビの表示名末尾の「（サンプル）」「（サンプル・架空データ）」は省く。
   ページのtitleそのものは変えない（検索・llms.txtはそのまま。省いた全文はツールチップに残す）。 */
var ZX_SUFFIX = /\s*（(使い方|テンプレート|サンプル[^）]*)）\s*$/;

function zxDecorateNav() {
  document.querySelectorAll(".md-nav--primary a.md-nav__link[href]").forEach(function (link) {
    if (link.dataset.zxTrimmed) return;
    link.dataset.zxTrimmed = "1";
    var label = link.querySelector(".md-ellipsis") || link;
    var node = label.firstChild;
    while (node && (node.nodeType !== Node.TEXT_NODE || !node.textContent.trim())) {
      node = node.nextSibling;
    }
    if (node && ZX_SUFFIX.test(node.textContent)) {
      link.title = node.textContent.trim();
      node.textContent = node.textContent.replace(ZX_SUFFIX, "");
    }
  });
}

/* 表の列見出しクリックで並べ替え（tablesort）。押印枠など class 付きの表は対象外 */
function zxSortableTables() {
  if (typeof Tablesort === "undefined") return;
  document.querySelectorAll("article table:not([class])").forEach(function (table) {
    if (table.dataset.zxSort || !table.tHead) return;
    table.dataset.zxSort = "1";
    new Tablesort(table);
  });
}

document$.subscribe(function () {
  zxDecorateNav();
  zxSortableTables();
});
