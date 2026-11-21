/**
 * PaceBowl — Zero-Dependency Pure-JS Vector PDF 1.4 Generator
 * Exports crisp, print-ready A4 Fridge Feeding Charts & Raw Batch Prep Sheets
 * with zero external libraries and 100% ASCII-safe WinAnsi typography.
 */
(function () {
  'use strict';

  function toAscii(str) {
    return String(str || '')
      .replace(/[×✕]/g, 'x')
      .replace(/[—–]/g, '-')
      .replace(/[•·]/g, '*')
      .replace(/[‘’]/g, "'")
      .replace(/[“”]/g, '"')
      .replace(/→/g, '->')
      .replace(/≥/g, '>=')
      .replace(/≤/g, '<=')
      .replace(/[^\x20-\x7E]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function pdfEsc(str) {
    return toAscii(str).replace(/\\/g, '\\\\').replace(/\(/g, '\\(').replace(/\)/g, '\\)');
  }

  function createBuilder() {
    const cmds = [];
    const rgb = (c) => c.map((v) => v.toFixed(3)).join(' ');
    return {
      rectFill(x, y, w, h, color) {
        cmds.push(`q ${rgb(color)} rg ${x.toFixed(1)} ${y.toFixed(1)} ${w.toFixed(1)} ${h.toFixed(1)} re f Q`);
      },
      rectStroke(x, y, w, h, color, lw) {
        cmds.push(`q ${rgb(color)} RG ${(lw || 0.8).toFixed(2)} w ${x.toFixed(1)} ${y.toFixed(1)} ${w.toFixed(1)} ${h.toFixed(1)} re S Q`);
      },
      line(x1, y1, x2, y2, color, lw) {
        cmds.push(`q ${rgb(color)} RG ${(lw || 0.6).toFixed(2)} w ${x1.toFixed(1)} ${y1.toFixed(1)} m ${x2.toFixed(1)} ${y2.toFixed(1)} l S Q`);
      },
      text(str, x, y, size, font, color) {
        cmds.push(`BT /${font || 'F1'} ${size.toFixed(1)} Tf ${rgb(color || [0.11, 0.11, 0.11])} rg ${x.toFixed(1)} ${y.toFixed(1)} Td (${pdfEsc(str)}) Tj ET`);
      },
      build() {
        return cmds.join('\n');
      },
    };
  }

  function buildPdfBlob(streamContent) {
    const objects = [
      '1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n',
      '2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n',
      '3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R >> >> /Contents 7 0 R >>\nendobj\n',
      '4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n',
      '5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n',
      '6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n',
      `7 0 obj\n<< /Length ${streamContent.length} >>\nstream\n${streamContent}\nendstream\nendobj\n`,
    ];
    let body = '%PDF-1.4\n';
    const offsets = [0];
    for (const o of objects) {
      offsets.push(body.length);
      body += o;
    }
    const xrefStart = body.length;
    body += `xref\n0 ${objects.length + 1}\n0000000000 65535 f \n`;
    for (let i = 1; i < offsets.length; i++) {
      body += String(offsets[i]).padStart(10, '0') + ' 00000 n \n';
    }
    body += `trailer\n<< /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xrefStart}\n%%EOF`;
    return new Blob([body], { type: 'application/pdf' });
  }

  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 4000);
  }

  /**
   * Generic Printable A4 Fridge Feeding Chart PDF
   * spec: { title, subtitle, filename, summaryRows: [[label, value]], tableHeaders: [..], tableRows: [[..]], checkboxes?: boolean, notes: [..] }
   */
  function downloadFeedingChartPdf(spec) {
    const b = createBuilder();
    const forest = [0.106, 0.263, 0.196];
    const amber = [0.851, 0.467, 0.024];
    const cream = [0.98, 0.972, 0.955];
    const charcoal = [0.11, 0.105, 0.10];
    const muted = [0.40, 0.39, 0.37];
    const border = [0.84, 0.83, 0.80];
    const white = [1, 1, 1];

    // Header Banner (A4 595 x 842 pt)
    b.rectFill(0, 760, 595, 82, forest);
    b.rectFill(0, 756, 595, 4, amber);
    b.text('PACEBOWL PET NUTRITION', 40, 804, 17, 'F2', white);
    b.text(spec.subtitle || 'PRINTABLE A4 FRIDGE FEEDING CHART  |  WSAVA & NRC STANDARDS', 40, 782, 8.5, 'F1', [0.85, 0.94, 0.89]);
    b.text(`Date: ${new Date().toISOString().slice(0, 10)}`, 468, 804, 8.5, 'F3', [0.85, 0.94, 0.89]);
    b.text('https://pacebowl.com', 450, 786, 8.5, 'F3', [0.99, 0.88, 0.55]);

    // Title
    b.text(spec.title || 'Custom Pet Feeding Chart', 40, 728, 15, 'F2', charcoal);
    b.line(40, 718, 555, 718, border, 0.8);

    // Summary Box
    const sumRows = spec.summaryRows || [];
    const boxH = Math.max(54, sumRows.length * 18 + 20);
    let y = 706 - boxH;
    b.rectFill(40, y, 515, boxH, cream);
    b.rectStroke(40, y, 515, boxH, border, 0.9);
    let sy = 706 - 20;
    for (const [k, v] of sumRows) {
      b.text(k, 52, sy, 9.5, 'F2', forest);
      b.text(v, 225, sy, 9.5, 'F1', charcoal);
      sy -= 18;
    }

    // Table Section
    y -= 26;
    if (spec.tableTitle) {
      b.text(spec.tableTitle, 40, y, 11, 'F2', charcoal);
      y -= 18;
    }

    const headers = spec.tableHeaders || [];
    const rows = spec.tableRows || [];
    if (headers.length && rows.length) {
      b.rectFill(40, y - 6, 515, 20, forest);
      const colW = 505 / headers.length;
      headers.forEach((h, idx) => {
        b.text(h, 46 + idx * colW, y, 8.5, 'F2', white);
      });
      y -= 22;

      rows.forEach((row, rIdx) => {
        if (y < 110) return;
        if (rIdx % 2 === 1) b.rectFill(40, y - 6, 515, 20, cream);
        b.line(40, y - 6, 555, y - 6, border, 0.4);
        row.forEach((cell, cIdx) => {
          const cx = 46 + cIdx * colW;
          if (spec.checkboxes && cIdx === headers.length - 1) {
            b.rectStroke(cx, y - 2, 9, 9, forest, 0.8);
            b.text('AM', cx + 12, y, 8, 'F1', muted);
            b.rectStroke(cx + 32, y - 2, 9, 9, forest, 0.8);
            b.text('PM', cx + 44, y, 8, 'F1', muted);
          } else {
            b.text(String(cell), cx, y, 8.5, cIdx === 0 ? 'F2' : 'F1', charcoal);
          }
        });
        y -= 20;
      });
    }

    // Veterinary Notes Box
    const notes = spec.notes || [
      'Always provide unlimited fresh, clean water alongside every meal.',
      'Weigh dry kibble or raw portions on a digital gram scale for +/-2% accuracy.',
      'Consult your veterinarian for pets with kidney, diabetic, or prescription diet needs.',
    ];
    const ny = Math.max(76, y - 16 - notes.length * 14 - 22);
    b.rectFill(40, ny, 515, notes.length * 14 + 26, cream);
    b.rectStroke(40, ny, 515, notes.length * 14 + 26, border, 0.7);
    b.text('FEEDING & SAFETY NOTES (POST ON FRIDGE)', 50, ny + notes.length * 14 + 10, 8.5, 'F2', forest);
    let nCursor = ny + notes.length * 14 - 4;
    for (const n of notes) {
      b.text(`* ${n}`, 50, nCursor, 8.2, 'F1', muted);
      nCursor -= 14;
    }

    // Footer
    b.line(40, 52, 555, 52, border, 0.7);
    b.text('PaceBowl Pet Nutrition Studio  |  Free Vet-Standard Portion & Slow-Feeder Calculators  |  https://pacebowl.com', 40, 36, 8, 'F1', muted);

    const blob = buildPdfBlob(b.build());
    downloadBlob(blob, spec.filename || 'PaceBowl-Feeding-Chart.pdf');
    try {
      if (window.umami && typeof window.umami.track === 'function') {
        const pathParts = (window.location && window.location.pathname ? window.location.pathname : '').split('/').filter(Boolean);
        const tool = pathParts[0] === 'tools' && pathParts[1] ? pathParts[1] : 'hub';
        window.umami.track('pacebowl_pdf_downloaded', {
          tool,
          filename: spec.filename || 'PaceBowl-Feeding-Chart.pdf',
        });
      }
    } catch (e) {}
  }

  // Track first real calculator interaction per tool per page load (for Calc -> PDF funnel rate)
  try {
    let engagedTracked = false;
    const trackEngagement = function (ev) {
      if (engagedTracked) return;
      if (!ev || !ev.target || !ev.target.closest || !ev.target.closest('.pb-calc-grid')) return;
      engagedTracked = true;
      if (window.umami && typeof window.umami.track === 'function') {
        const pathParts = (window.location && window.location.pathname ? window.location.pathname : '').split('/').filter(Boolean);
        const tool = pathParts[0] === 'tools' && pathParts[1] ? pathParts[1] : 'hub';
        window.umami.track('pacebowl_calculator_used', { tool });
      }
    };
    if (typeof document !== 'undefined' && document.addEventListener) {
      document.addEventListener('change', trackEngagement, true);
      document.addEventListener('input', trackEngagement, true);
    }
  } catch (e) {}

  window.PaceBowlPdf = { downloadFeedingChartPdf };
})();
