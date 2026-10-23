---
name: terminal-replica
description: >
  Reproduce YOUR real terminal and CLI agents (Claude Code, Codex CLI, Gemini
  CLI) faithfully in any generated graphic, GIF, or video frame. Use whenever
  an asset shows a terminal, an agent transcript, a statusline, or a CLI
  banner. Capture your actual theme, font, prompt and statusline first, and
  never invent a generic "hacker terminal" look.
---

# Terminal replica

Terminal-like graphics must match the real tool and the real setup of the person who ships the asset. A generic green-on-black "hacker terminal" reads as fake. This skill is a method for capturing your own setup, plus a render recipe and a worked example.

## Method

1. Capture the ground truth. Take a fresh screenshot of your real terminal running the tool. Sample background, foreground and accent colors from it with an eyedropper or `PIL.Image.getpixel`. A live screenshot beats any spec in this file.
2. Record these five facts about your setup:
   - Emulator (Terminal.app, iTerm2, Warp, the VS Code integrated terminal, Ghostty).
   - Font family and size. Check the emulator's settings. VS Code on macOS defaults to Menlo 12.
   - Theme: background, default foreground, and the 16 ANSI colors.
   - Shell prompt shape (for example `user@host ~ %` for default macOS zsh, or your powerline or starship layout).
   - Statusline format, if your agent has a custom one.
3. Use your own session logs for transcript shapes. Claude Code stores them at `~/.claude/projects/<project-slug>/*.jsonl`. The assistant and tool-use turns show exactly what text appears.
4. Draw from those facts, then verify by placing the render next to a real screenshot before you publish.

Keep a small config in your own project (a JSON or Python dict) holding the five facts, and read it from your render scripts. Do not hardcode them in shared code.

## Claude Code TUI

Layout top to bottom on launch (verify against your installed version):

1. A pixel-art logo on the left: a blocky creature in Anthropic terracotta (`#D97757`), roughly 5x4 fat pixels with feet. Do not redraw it as an emoji or a robot.
2. A header text block to its right: `Claude Code` in bold white plus the version in gray, a gray model and account line, and a gray working-directory path.
3. Warnings: a warning glyph plus orange-yellow text (for example "N MCP servers need authentication") and a gray `· run /mcp`.
4. Notice blocks: an orange left border `│`, an orange bold title line, the body in the default foreground, and underlined blue links.
5. Prompt: `❯` then a dim gray placeholder with a block cursor over its first character.
6. Statusline at the bottom, one line, if you have configured one. Draw exactly your own format, including filled bars in green and empty bars dimmed.
7. Mode line below the statusline when a permission mode is active (for example "bypass permissions on (shift+tab to cycle)").

Transcript shapes (session JSONL to TUI rendering):

- Assistant tool call: `⏺ Bash(git status)`, with the dot colored (green when ok), the tool name white and the args dim.
- Result continuation: `  ⎿  <first line of output>` dim, and `… +N lines` in gray.
- Working spinner: a single animated glyph cycling `✳ ✶ ✻ ✽`, plus a gerund word ("Reticulating…") and a gray token count.
- User turn: `>` followed by plain text.
- Never show affordances that do not exist: no tabs, no menu bar, no fake buttons inside the TUI.

Animation notes for GIF and video: the cursor blinks as a square block at about 530ms, the spinner steps at about 120ms, and output appears in whole-line chunks. Only the user's typing appears character by character.

## Codex CLI

- Invoked as `codex` in the same terminal, so the same background and font as above.
- Banner: a minimal `>_ OpenAI Codex (vX.Y.Z)` style header line with a blue accent, then a bordered input box drawn with rounded box-drawing characters (`╭─╮ │ ╰─╯`) and a dim placeholder such as "Ask Codex to do anything".
- A dim gray shortcuts line at the bottom.
- Verify live before shipping: run `codex` yourself in a scratch directory and screenshot it. Check `~/.codex/config.toml` for a custom theme.

## Gemini CLI

- Do not fake it from memory. If an asset needs it, install it in a scratch environment (`npm i -g @google/gemini-cli`), run it and screenshot it.
- Known shape if you cannot verify: a large `GEMINI` ASCII banner in a blue to purple gradient, a tips list, a bordered input box (`> Type your message`), and a bottom status line with cwd, sandbox note, model name and context percent. Mark any unverified render as a draft.

## Render recipe (PIL)

- Render at 2x, then downscale 50% with LANCZOS for anti-aliasing.
- Mono font from your captured setup (`/System/Library/Fonts/Menlo.ttc` on macOS if that is what you use). Draw TUI glyphs that your font lacks (record dot, elbow, spinner) as vector shapes. Never ship tofu boxes.
- Line height about 1.35em, left padding about 2 characters, no drop shadows inside the terminal.
- Window chrome: either a flat panel matching your emulator, or crop the chrome entirely and show only content.

## Example values

An example only, taken from a typical VS Code Dark Modern setup. Replace every value with what you captured in the Method section.

- Emulator: VS Code integrated terminal. Font: Menlo 12.
- Background `#181818`, default foreground `#CCCCCC`.
- ANSI normal: black `#000000`, red `#CD3131`, green `#0DBC79`, yellow `#E5E510`, blue `#2472C8`, magenta `#BC3FBC`, cyan `#11A8CD`, white `#E5E5E5`.
- ANSI bright: `#666666` `#F14C4C` `#23D18B` `#F5F543` `#3B8EEA` `#D670D6` `#29B8DB` `#FFFFFF`.
- Prompt: `user@host ~ %`.
- Statusline (a custom one): `🤖 Model | ctx: 0% | s:▰▰▰▰▰ 87% | $4.06`, with filled bars in green `#23D18B` and empty bars dim.

## Definition of done

- [ ] Colors sampled from a real screenshot of your own terminal, or matched to your captured config
- [ ] The mono font matches your emulator, with no emoji-style logo substitutes
- [ ] Transcript lines copied or adapted from a real session log
- [ ] The statusline matches your own format if shown
- [ ] Codex and Gemini banners verified live, or explicitly flagged as unverified
