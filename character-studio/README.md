# Jolly-bot Character Studio

A single-file web tool for designing the robot's body language before any hardware exists.
Type a line the robot says, get three animated options rendered in three.js on the real six channels
(yaw, pitch, roll, bob, two arm flaps, plus cheek glow and catchlight blinks), keep the one that fits,
and the pick and your notes go into a "character bible" that steers the next round.

Published as a claude.ai artifact, where the page asks Claude for the three variants and keeps the bible
in the artifact's store. Opened as a plain file it still runs: the Design button then composes from the
built-in motion library and picks stay in the tab.

Every generated clip is clamped to the hardware limits from `cad/jollybot/analysis/TORQUE_CHECK.md`
(ranges, speeds, combined-tilt cap) and can be downloaded as JSON for the animation engine on the Pi.
