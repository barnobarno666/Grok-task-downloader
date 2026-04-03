// ==UserScript==
// @name         Grok Single Task to Markdown Exporter (Fix)
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  Extracts the current Grok task output directly to a Markdown file.
// @match        https://grok.com/*
// @require      https://unpkg.com/turndown/dist/turndown.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Grok uses Tailwind's typography plugin for rendered markdown
    const TARGET_SELECTOR = '.prose';

    function exportToMarkdown() {
        const proseNodes = document.querySelectorAll(TARGET_SELECTOR);

        if (!proseNodes || proseNodes.length === 0) {
            console.error('Target node not found. DOM structure: ', document.body.innerHTML.substring(0, 500));
            alert('Could not find the content area. Wait for hydration or check if Grok altered their CSS classes.');
            return;
        }

        // Isolate the markdown content into a standalone wrapper to prevent mutating the live SPA
        const cloneWrapper = document.createElement('div');
        proseNodes.forEach((node, index) => {
            cloneWrapper.appendChild(node.cloneNode(true));
            // Separate multiple blocks (e.g., prompt and response) with a horizontal rule
            if (index < proseNodes.length - 1) {
                const hr = document.createElement('hr');
                cloneWrapper.appendChild(hr);
            }
        });

        // Strip out any trailing interactive SVGs or copy buttons embedded inside the prose block
        const removeSelectors = ['button', 'svg', '.group\\/copy-button'];
        removeSelectors.forEach(sel => {
            cloneWrapper.querySelectorAll(sel).forEach(el => el.remove());
        });

        const turndownService = new TurndownService({
            headingStyle: 'atx',
            codeBlockStyle: 'fenced',
            emDelimiter: '*'
        });

        // Retain code language tags for syntax highlighting (e.g., ```python)
        turndownService.addRule('preCode', {
            filter: ['pre'],
            replacement: function (content, node) {
                // Grok usually nests <code> inside <pre>, often with a language class
                const codeNode = node.querySelector('code');
                let lang = '';
                if (codeNode && codeNode.className) {
                    const match = codeNode.className.match(/language-(\w+)/);
                    if (match) lang = match[1];
                }
                return '\n```' + lang + '\n' + node.textContent.trim() + '\n```\n';
            }
        });

        const markdown = turndownService.turndown(cloneWrapper);

        // Generate the blob and execute download
        const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        a.href = url;
        a.download = `Grok_Task_${timestamp}.md`;

        document.body.appendChild(a);
        a.click();

        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
    }

    function injectButton() {
        if (document.getElementById('grok-md-exporter')) return;

        const btn = document.createElement('button');
        btn.id = 'grok-md-exporter';
        btn.innerText = '↓ Download MD';
        btn.style.cssText = `
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 999999;
            padding: 8px 16px;
            background: #2ea043;
            color: #ffffff;
            border: 1px solid #238636;
            border-radius: 6px;
            font-family: monospace;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: background 0.2s;
        `;

        btn.onmouseover = () => btn.style.background = '#3fb950';
        btn.onmouseout = () => btn.style.background = '#2ea043';
        btn.onclick = exportToMarkdown;

        document.body.appendChild(btn);
    }

    // Use a MutationObserver instead of a hard timeout to handle Next.js client-side routing more robustly
    const observer = new MutationObserver(() => {
        if (!document.getElementById('grok-md-exporter')) {
            injectButton();
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
})();