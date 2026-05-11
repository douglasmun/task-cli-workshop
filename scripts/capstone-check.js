#!/usr/bin/env node
// Capstone check script for the Claude Code course starter repo.
// Run: npm run capstone-check
// Checks that all required capstone artifacts exist and have correct structure.

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

const GREEN  = '\x1b[32m';
const RED    = '\x1b[31m';
const YELLOW = '\x1b[33m';
const RESET  = '\x1b[0m';
const BOLD   = '\x1b[1m';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function exists(relPath) {
  return fs.existsSync(path.join(ROOT, relPath));
}

function readText(relPath) {
  const abs = path.join(ROOT, relPath);
  if (!fs.existsSync(abs)) return null;
  return fs.readFileSync(abs, 'utf8');
}

function isValidJSON(relPath) {
  const text = readText(relPath);
  if (text === null) return { valid: false, data: null };
  try {
    return { valid: true, data: JSON.parse(text) };
  } catch (_) {
    return { valid: false, data: null };
  }
}

function countLines(relPath) {
  const text = readText(relPath);
  if (text === null) return 0;
  return text.split('\n').filter(l => l.trim() !== '').length;
}

function isDir(relPath) {
  const abs = path.join(ROOT, relPath);
  return fs.existsSync(abs) && fs.statSync(abs).isDirectory();
}

function subdirs(relPath) {
  const abs = path.join(ROOT, relPath);
  if (!fs.existsSync(abs)) return [];
  return fs.readdirSync(abs).filter(name => {
    return fs.statSync(path.join(abs, name)).isDirectory();
  });
}

function filesWithExt(relDir, ext) {
  const abs = path.join(ROOT, relDir);
  if (!fs.existsSync(abs)) return [];
  return fs.readdirSync(abs).filter(name => name.endsWith(ext));
}

// ---------------------------------------------------------------------------
// Core Pass checks (11 checks)
// ---------------------------------------------------------------------------

function checkClaudeMdExists() {
  const lines = countLines('CLAUDE.md');
  if (lines > 10) return { pass: true };
  return {
    pass: false,
    hint: 'Create CLAUDE.md with at least 10 non-blank lines describing your project.',
  };
}

function checkClaudeMdAtRef() {
  const text = readText('CLAUDE.md');
  if (text && /@[^\s]/.test(text)) return { pass: true };
  return {
    pass: false,
    hint: 'Add an @file reference in CLAUDE.md (e.g. "See @docs/architecture.md").',
  };
}

function checkSkillsMinThree() {
  const dirs = subdirs('.claude/skills');
  if (dirs.length >= 3) return { pass: true };
  return {
    pass: false,
    hint: `Found ${dirs.length} skill(s) — need at least 3 in .claude/skills/.`,
  };
}

function checkSkillHasArguments() {
  const dirs = subdirs('.claude/skills');
  for (const dir of dirs) {
    const text = readText(`.claude/skills/${dir}/SKILL.md`);
    if (text && text.includes('$ARGUMENTS')) return { pass: true };
  }
  return {
    pass: false,
    hint: 'At least one SKILL.md must reference $ARGUMENTS in its body.',
  };
}

function checkSkillHasForkContext() {
  const dirs = subdirs('.claude/skills');
  for (const dir of dirs) {
    const text = readText(`.claude/skills/${dir}/SKILL.md`);
    if (text && /context:\s*fork/.test(text)) return { pass: true };
  }
  return {
    pass: false,
    hint: 'At least one SKILL.md must have "context: fork" in its frontmatter.',
  };
}

function checkAgentFileExists() {
  const files = filesWithExt('.claude/agents', '.md');
  if (files.length >= 1) return { pass: true };
  return {
    pass: false,
    hint: 'Create at least one agent .md file in .claude/agents/.',
  };
}

function checkAgentMemoryUser() {
  const files = filesWithExt('.claude/agents', '.md');
  for (const file of files) {
    const text = readText(`.claude/agents/${file}`);
    if (text && /memory:\s*user/.test(text)) return { pass: true };
  }
  return {
    pass: false,
    hint: 'At least one agent .md must contain "memory: user" in its frontmatter.',
  };
}

function checkFormatHook() {
  const text = readText('.claude/hooks/format-file.sh');
  if (text && text.trim().length > 0) return { pass: true };
  return {
    pass: false,
    hint: 'Create a non-empty .claude/hooks/format-file.sh.',
  };
}

function checkBlockHook() {
  const text = readText('.claude/hooks/block-dangerous-bash.sh');
  if (text && text.trim().length > 0) return { pass: true };
  return {
    pass: false,
    hint: 'Create a non-empty .claude/hooks/block-dangerous-bash.sh.',
  };
}

function checkSettingsHooks() {
  const { valid, data } = isValidJSON('.claude/settings.json');
  if (!valid) {
    return { pass: false, hint: '.claude/settings.json is missing or not valid JSON.' };
  }
  const text = JSON.stringify(data);
  const hasPost = text.includes('PostToolUse');
  const hasPre  = text.includes('PreToolUse');
  if (hasPost && hasPre) return { pass: true };
  const missing = [!hasPost && 'PostToolUse', !hasPre && 'PreToolUse'].filter(Boolean).join(', ');
  return {
    pass: false,
    hint: `.claude/settings.json is missing hooks: ${missing}.`,
  };
}

function checkMcpJson() {
  const { valid, data } = isValidJSON('.mcp.json');
  if (!valid) {
    return { pass: false, hint: '.mcp.json is missing or not valid JSON.' };
  }
  if (data && typeof data.mcpServers === 'object') return { pass: true };
  return {
    pass: false,
    hint: '.mcp.json must have a top-level "mcpServers" key.',
  };
}

// ---------------------------------------------------------------------------
// Professional Pass checks (2 checks)
// ---------------------------------------------------------------------------

function checkPluginJson() {
  const { valid, data } = isValidJSON('plugin/.claude-plugin/plugin.json');
  if (valid && data) return { pass: true };
  return {
    pass: false,
    hint: 'Create plugin/.claude-plugin/plugin.json as valid JSON.',
  };
}

function checkGithubWorkflows() {
  const ymls = filesWithExt('.github/workflows', '.yml');
  if (ymls.length >= 1) return { pass: true };
  return {
    pass: false,
    hint: 'Add at least one .yml workflow file in .github/workflows/.',
  };
}

// ---------------------------------------------------------------------------
// Native/Team Pass checks (4 checks)
// ---------------------------------------------------------------------------

function checkCoworkAboutMe() {
  if (countLines('cowork/about-me.md') > 3) return { pass: true };
  return {
    pass: false,
    hint: 'cowork/about-me.md must exist and have more than 3 non-blank lines.',
  };
}

function checkCoworkBrandVoice() {
  if (countLines('cowork/brand-voice.md') > 3) return { pass: true };
  return {
    pass: false,
    hint: 'cowork/brand-voice.md must exist and have more than 3 non-blank lines.',
  };
}

function checkCoworkWorkingPreferences() {
  if (countLines('cowork/working-preferences.md') > 3) return { pass: true };
  return {
    pass: false,
    hint: 'cowork/working-preferences.md must exist and have more than 3 non-blank lines.',
  };
}

function checkCoworkPlugin() {
  const { valid, data } = isValidJSON('cowork/plugin/.claude-plugin/plugin.json');
  if (valid && data) return { pass: true };
  return {
    pass: false,
    hint: 'Create cowork/plugin/.claude-plugin/plugin.json as valid JSON.',
  };
}

// ---------------------------------------------------------------------------
// Runner
// ---------------------------------------------------------------------------

function runCheck(description, checkFn) {
  const result = checkFn();
  if (result.pass) {
    process.stdout.write(`  ${GREEN}✓${RESET}  ${description}\n`);
  } else {
    process.stdout.write(`  ${RED}✗${RESET}  ${description}\n`);
    if (result.hint) {
      process.stdout.write(`       ${YELLOW}hint:${RESET} ${result.hint}\n`);
    }
  }
  return result.pass;
}

function passLabel(pass) {
  return pass
    ? `${GREEN}${BOLD}PASS${RESET}`
    : `${RED}${BOLD}FAIL${RESET}`;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

process.stdout.write(`\n  ${BOLD}Capstone Check — Claude Code Course${RESET}\n\n`);

// Core Pass (11 checks)
process.stdout.write(`  ${BOLD}── Core Pass ──────────────────────────────────────────${RESET}\n`);
const coreResults = [
  runCheck('CLAUDE.md exists and has content (> 10 lines)',           checkClaudeMdExists),
  runCheck('CLAUDE.md contains an @ file reference',                  checkClaudeMdAtRef),
  runCheck('.claude/skills/ has at least 3 subdirectories',           checkSkillsMinThree),
  runCheck('At least one skill has $ARGUMENTS in its SKILL.md',       checkSkillHasArguments),
  runCheck('At least one skill has context: fork in its frontmatter', checkSkillHasForkContext),
  runCheck('.claude/agents/ has at least one .md file',               checkAgentFileExists),
  runCheck('At least one agent file contains memory: user',           checkAgentMemoryUser),
  runCheck('.claude/hooks/format-file.sh exists and is non-empty',    checkFormatHook),
  runCheck('.claude/hooks/block-dangerous-bash.sh exists and is non-empty', checkBlockHook),
  runCheck('.claude/settings.json contains PostToolUse and PreToolUse', checkSettingsHooks),
  runCheck('.mcp.json is valid JSON with mcpServers key',             checkMcpJson),
];
const corePassed = coreResults.filter(Boolean).length;
const corePass   = corePassed === 11;

// Professional Pass (2 checks)
process.stdout.write(`\n  ${BOLD}── Professional Pass ──────────────────────────────────${RESET}\n`);
const profResults = [
  runCheck('plugin/.claude-plugin/plugin.json exists and is valid JSON', checkPluginJson),
  runCheck('.github/workflows/ has at least one .yml file',              checkGithubWorkflows),
];
const profPassed = profResults.filter(Boolean).length;
const profPass   = profPassed === 2;

// Native/Team Pass (4 checks)
process.stdout.write(`\n  ${BOLD}── Native/Team Pass ───────────────────────────────────${RESET}\n`);
const nativeResults = [
  runCheck('cowork/about-me.md exists and has > 3 lines',                   checkCoworkAboutMe),
  runCheck('cowork/brand-voice.md exists and has > 3 lines',                checkCoworkBrandVoice),
  runCheck('cowork/working-preferences.md exists and has > 3 lines',        checkCoworkWorkingPreferences),
  runCheck('cowork/plugin/.claude-plugin/plugin.json exists and is valid JSON', checkCoworkPlugin),
];
const nativePassed = nativeResults.filter(Boolean).length;
const nativePass   = nativePassed === 4;

// Summary
const profNote   = corePass  ? '' : ' — requires Core Pass';
const nativeNote = profPass  ? '' : ' — requires Professional Pass';

process.stdout.write('\n');
process.stdout.write(`  Core Pass:         ${corePassed} / 11  [${passLabel(corePass)}]\n`);
process.stdout.write(`  Professional Pass: ${profPassed} / 2   [${passLabel(profPass)}${profNote}]\n`);
process.stdout.write(`  Native/Team Pass:  ${nativePassed} / 4   [${passLabel(nativePass)}${nativeNote}]\n`);
process.stdout.write('\n');

process.exit(corePass ? 0 : 1);
