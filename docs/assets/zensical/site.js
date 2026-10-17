/* =============================================================================
   Zensical版専用スクリプト（正本の javascripts/extra.js の後に読み込む）
   document$ はインスタントナビゲーションでページが切り替わるたびに発火する。
   ============================================================================= */

/* ナビの各ページを、ファイル名の接頭辞（[使い方]／[Template]／[Sample]）で色バッジ付けする。
   「CRUD表（使い方）」のように表示名末尾にある種別の括弧書きはバッジと重複するので隠す。
   ページのtitleそのものは変えない（検索・llms.txtはそのまま）。 */
var ZX_SUFFIX = /\s*（(使い方|テンプレート|サンプル[^）]*)）\s*$/;

function zxDecorateNav() {
  document.querySelectorAll(".md-nav--primary a.md-nav__link[href]").forEach(function (link) {
    if (link.dataset.zxKind) return;
    var href = decodeURIComponent(link.getAttribute("href"));
    var m = href.match(/\[(使い方|Template|Sample)\]/);
    if (!m) return;
    link.dataset.zxKind = m[1];
    var label = link.querySelector(".md-ellipsis") || link;
    label.classList.add("zx-kind");
    label.dataset.zxKind = m[1];
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
