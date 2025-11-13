function fix_title(frm,translated_name) {
    if (!frm.doc.__islocal) return;

    const base = (frm.meta && frm.meta.translated_name) ? frm.meta.translated_name : translated_name;
    const desired = 'Nouvelle ' + base;

    const patterns = [
        'Nouveau ' + base,
        'Nouveau '+translated_name,
        'Nouveau ' + (frm.doc.doctype || '')
    ];

    // sélecteurs ciblés
    const selectors = [
        '.page-head .title-text',
        '.page-title .title-text',
        'h1[data-doctype]',
        'h3.page-title',
        '.document-title',
        '.page-head .breadcrumb .active',
        '.breadcrumb .breadcrumb-item',
        '.breadcrumb .active',
        '#navbar-breadcrumbs li.disabled a',
        '#navbar-breadcrumbs li a[href*="new-"]'        
    ];

    function escapeRegExp(s) {
        return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    const regex = new RegExp(patterns.map(escapeRegExp).join('|'), 'g');

    function replaceInElement(el) {
        if (!el || !el.textContent) return false;
        const txt = el.textContent.trim();
        if (!txt) return false;
        if (regex.test(txt)) {
            el.textContent = txt.replace(regex, desired);
            return true;
        }
        return false;
    }

    let changed = false;
    selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
            if (replaceInElement(el)) changed = true;
        });
    });
    if (document.title && regex.test(document.title)) {
        document.title = document.title.replace(regex, desired);
        changed = true;
    }
    if (changed) return; 
    const root = document.querySelector('.page-head') || document.querySelector('body');
    if (root) {
        const obs = new MutationObserver((mutations, observer) => {
            let made = false;
            selectors.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => {
                    if (replaceInElement(el)) made = true;
                });
            });
            if (document.title && regex.test(document.title)) {
                document.title = document.title.replace(regex, desired);
                made = true;
            }
            if (made) {
                observer.disconnect(); 
            }
        });
        obs.observe(root, { childList: true, subtree: true, characterData: true });
        setTimeout(() => obs.disconnect(), 2000);
    }

    let frames = 0, maxFrames = 60; 
    function rafLoop() {
        let made = false;
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => {
                if (replaceInElement(el)) made = true;
            });
        });
        if (document.title && regex.test(document.title)) {
            document.title = document.title.replace(regex, desired);
            made = true;
        }
        if (!made && frames++ < maxFrames) {
            requestAnimationFrame(rafLoop);
        }
    }
    requestAnimationFrame(rafLoop);
}



// Pour les formulaires en QUICK ENTRY 
function applyFemaleTitleFix(translated, root) {
  try {
    if (!translated) return false;
    const escapeForRegex = s => s.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&');

    function replaceInTextNodes(r, regex, replacement) {
      if (!r) return false;
      const walker = document.createTreeWalker(r, NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
          if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
          const parent = node.parentNode;
          if (!parent) return NodeFilter.FILTER_REJECT;
          const tag = parent.tagName ? parent.tagName.toLowerCase() : '';
          if (['input', 'textarea', 'select'].includes(tag)) return NodeFilter.FILTER_REJECT;
          if (parent.isContentEditable) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      }, false);

      let node, changed = false;
      while ((node = walker.nextNode())) {
        if (regex.test(node.nodeValue)) {
          node.nodeValue = node.nodeValue.replace(regex, replacement);
          changed = true;
        }
      }
      return changed;
    }

    const SAFE_SELECTORS = [
      '.modal .modal-title',
      '.modal .modal-header h5',
      '.modal .modal-header .modal-title',
      '.modal .modal-body label',
      '.modal .modal-body span',
      '.modal .modal-body button',
      '.modal .modal-body a'
    ];

    const rootEl = root || document;
    const safeName = escapeForRegex(translated);
    const regex = new RegExp('\\bNouveau\\s+' + safeName + '\\b', 'g');
    const desired = 'Nouvelle ' + translated;
    let made = false;

    SAFE_SELECTORS.forEach(sel => {
      (rootEl.querySelectorAll ? rootEl.querySelectorAll(sel) : []).forEach(el => {
        try {
          if (!el.querySelector || !el.querySelector('input,textarea,select')) {
            if (regex.test(el.textContent || '')) {
              el.textContent = (el.textContent || '').replace(regex, desired);
              made = true;
            }
          } else {
            if (replaceInTextNodes(el, regex, desired)) made = true;
          }
        } catch (e) { /* ignore */ }
      });
    });

    if (replaceInTextNodes(rootEl, regex, desired)) made = true;
    return made;
  } catch (e) {
    console.error('fr-title-fixer: applyFemaleTitleFix error', e);
    return false;
  }
}


// Pour les formulaires en QUICK ENTRY 
function applyMaleTitleFix(translated, root) {
  try {
    if (!translated) return false;
    const escapeForRegex = s => s.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&');

    function replaceInTextNodes(r, regex, replacement) {
      if (!r) return false;
      const walker = document.createTreeWalker(r, NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
          if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
          const parent = node.parentNode;
          if (!parent) return NodeFilter.FILTER_REJECT;
          const tag = parent.tagName ? parent.tagName.toLowerCase() : '';
          if (['input', 'textarea', 'select'].includes(tag)) return NodeFilter.FILTER_REJECT;
          if (parent.isContentEditable) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      }, false);

      let node, changed = false;
      while ((node = walker.nextNode())) {
        if (regex.test(node.nodeValue)) {
          node.nodeValue = node.nodeValue.replace(regex, replacement);
          changed = true;
        }
      }
      return changed;
    }

    const SAFE_SELECTORS = [
      '.modal .modal-title',
      '.modal .modal-header h5',
      '.modal .modal-header .modal-title',
      '.modal .modal-body label',
      '.modal .modal-body span',
      '.modal .modal-body button',
      '.modal .modal-body a'
    ];

    const rootEl = root || document;
    const safeName = escapeForRegex(translated);
    const regex = new RegExp('\\bNouveau\\s+' + safeName + '\\b', 'g');
    const desired = 'Nouvel ' + translated;
    let made = false;

    SAFE_SELECTORS.forEach(sel => {
      (rootEl.querySelectorAll ? rootEl.querySelectorAll(sel) : []).forEach(el => {
        try {
          if (!el.querySelector || !el.querySelector('input,textarea,select')) {
            if (regex.test(el.textContent || '')) {
              el.textContent = (el.textContent || '').replace(regex, desired);
              made = true;
            }
          } else {
            if (replaceInTextNodes(el, regex, desired)) made = true;
          }
        } catch (e) { /* ignore */ }
      });
    });

    if (replaceInTextNodes(rootEl, regex, desired)) made = true;
    return made;
  } catch (e) {
    console.error('fr-title-fixer: applyFemaleTitleFix error', e);
    return false;
  }
}