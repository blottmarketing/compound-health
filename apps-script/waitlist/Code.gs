/**
 * Compound Health waitlist: receives POSTs from the access form on
 * compoundhealth.io and writes them into this spreadsheet.
 *
 * Two tabs, one per audience, so client requests and partner enquiries never
 * mix. Run `setup()` once from the editor to create and format the tabs.
 * Deploy as a web app (Execute as: Me, Who has access: Anyone) and paste the
 * /exec URL into WAITLIST_ENDPOINT in src/pages/index.astro.
 */

// Optional: an address that gets a short email on every new submission.
// Leave empty to disable.
const NOTIFY_EMAIL = '';

const SHEETS = {
  client: {
    name: 'Clients',
    columns: [
      'Submitted at', 'First name', 'Last name', 'Email', 'Membership tier',
      'Referring advisor or firm', 'Source', 'User agent',
    ],
    widths: [170, 130, 130, 240, 130, 220, 150, 320],
    row: (p) => [
      p.submittedAt, p.firstName, p.lastName, p.email, p.tier, p.advisor,
      p.source, p.userAgent,
    ],
  },
  partner: {
    name: 'Partners',
    columns: [
      'Submitted at', 'Type', 'Organization', 'First name', 'Last name', 'Email',
      'People you would introduce', 'Source', 'User agent',
    ],
    widths: [170, 190, 220, 130, 130, 240, 170, 150, 320],
    row: (p) => [
      p.submittedAt, p.role, p.organization, p.firstName, p.lastName, p.email,
      p.reach, p.source, p.userAgent,
    ],
  },
};

// Slugs sent by the form, mapped to the labels shown on the site.
const LABELS = {
  role: {
    'client': 'A client',
    'wealth-firm': 'A wealth firm',
    'employer': 'An employer',
    'network': 'A network or organization',
  },
  tier: { baseline: 'Baseline', optimize: 'Optimize', eternal: 'Eternal' },
  reach: {
    'under-100': 'Under 100',
    '100-500': '100 to 500',
    '500-2000': '500 to 2,000',
    'over-2000': 'Over 2,000',
  },
};

const HEADER_BG = '#2f4a16';   // dark green, matches the site button
const HEADER_FG = '#ffffff';
const BAND_BG   = '#f1efea';   // --panel

/* ---------------------------------------------------------------- HTTP */

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const p = normalise(e && e.parameter ? e.parameter : {});
    if (!p.email) return respond(400, 'Email is required.');

    const config = SHEETS[p.audience] || SHEETS.client;
    const sheet = getOrCreateSheet(config);
    sheet.appendRow(config.row(p));
    formatLastRow(sheet, config);

    if (NOTIFY_EMAIL) notify(p, config);
    return respond(200, 'ok');
  } catch (err) {
    console.error(err);
    return respond(500, String(err));
  } finally {
    lock.releaseLock();
  }
}

// Health check: opening the /exec URL in a browser should show this.
function doGet() {
  return respond(200, 'Compound Health waitlist endpoint is live.');
}

function respond(status, message) {
  return ContentService
    .createTextOutput(JSON.stringify({ status, message }))
    .setMimeType(ContentService.MimeType.JSON);
}

/* ---------------------------------------------------------------- Data */

function normalise(q) {
  const clean = (v) => String(v || '').trim();
  const label = (map, v) => map[clean(v)] || clean(v);
  const submitted = clean(q.submittedAt);
  const date = submitted ? new Date(submitted) : new Date();

  return {
    submittedAt:  isNaN(date.getTime()) ? new Date() : date,
    audience:     clean(q.audience) === 'partner' ? 'partner' : 'client',
    role:         label(LABELS.role, q.role),
    firstName:    clean(q.firstName),
    lastName:     clean(q.lastName),
    email:        clean(q.email).toLowerCase(),
    tier:         label(LABELS.tier, q.tier),
    advisor:      clean(q.advisor),
    organization: clean(q.organization),
    reach:        label(LABELS.reach, q.reach),
    source:       clean(q.source) || 'compoundhealth.io',
    userAgent:    clean(q.userAgent),
  };
}

/* ---------------------------------------------------------------- Sheet */

/** Run once from the editor. Creates and formats both tabs, removes the default 'Sheet1'. */
function setup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  Object.values(SHEETS).forEach((config) => getOrCreateSheet(config));

  const leftover = ss.getSheetByName('Sheet1') || ss.getSheetByName('List1');
  if (leftover && ss.getSheets().length > 1 && leftover.getLastRow() === 0) {
    ss.deleteSheet(leftover);
  }
  ss.setActiveSheet(ss.getSheetByName(SHEETS.client.name));
}

function getOrCreateSheet(config) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(config.name);
  if (!sheet) sheet = ss.insertSheet(config.name);
  if (sheet.getLastRow() === 0) formatHeader(sheet, config);
  return sheet;
}

function formatHeader(sheet, config) {
  const n = config.columns.length;
  const header = sheet.getRange(1, 1, 1, n);

  header.setValues([config.columns])
    .setBackground(HEADER_BG)
    .setFontColor(HEADER_FG)
    .setFontWeight('bold')
    .setFontFamily('Lato')
    .setVerticalAlignment('middle');
  sheet.setRowHeight(1, 36);
  sheet.setFrozenRows(1);

  config.widths.forEach((w, i) => sheet.setColumnWidth(i + 1, w));

  // Trim unused columns so the tab reads as a table, not an endless grid.
  const maxCols = sheet.getMaxColumns();
  if (maxCols > n) sheet.deleteColumns(n + 1, maxCols - n);

  // Filter on the header, banding on the body.
  sheet.getRange(1, 1, sheet.getMaxRows(), n).createFilter();
  const banding = sheet.getRange(2, 1, sheet.getMaxRows() - 1, n)
    .applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, false, false);
  banding.setFirstRowColor('#ffffff').setSecondRowColor(BAND_BG);

  // Date column, and a plain-text body so nothing gets auto-converted.
  sheet.getRange(2, 1, sheet.getMaxRows() - 1, 1).setNumberFormat('yyyy-mm-dd hh:mm');
  sheet.getRange(2, 2, sheet.getMaxRows() - 1, n - 1).setNumberFormat('@');
  sheet.getRange(2, 1, sheet.getMaxRows() - 1, n)
    .setFontFamily('Lato')
    .setVerticalAlignment('middle')
    .setWrap(false);
}

function formatLastRow(sheet, config) {
  const r = sheet.getLastRow();
  const n = config.columns.length;
  sheet.setRowHeight(r, 28);
  sheet.getRange(r, 1).setNumberFormat('yyyy-mm-dd hh:mm');
  sheet.getRange(r, 1, 1, n).setFontFamily('Lato').setVerticalAlignment('middle').setWrap(false);
  // Newest first is easier to scan.
  sheet.getRange(2, 1, r - 1, n).sort({ column: 1, ascending: false });
}

/* ---------------------------------------------------------------- Email */

function notify(p, config) {
  const who = p.audience === 'partner'
    ? `${p.role}: ${p.organization}`
    : `Client, ${p.tier}`;
  const subject = `New waitlist submission: ${p.firstName} ${p.lastName} (${who})`;
  const lines = config.columns.map((c, i) => {
    const v = config.row(p)[i];
    return `${c}: ${v instanceof Date ? Utilities.formatDate(v, Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm') : v}`;
  });
  lines.push('', SpreadsheetApp.getActiveSpreadsheet().getUrl());
  MailApp.sendEmail(NOTIFY_EMAIL, subject, lines.join('\n'));
}
