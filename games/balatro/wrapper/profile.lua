-- Balatro on love-mini. The game is the player's own (Balatro.exe or Balatro.love in this
-- folder): nothing of it is here. What is here makes it fit the Mini, as PortMaster's
-- Balatro port does on other handhelds (its patches, MIT, in lua/portmaster/; see
-- licenses/): the small-screen layout for 640x480, lighter graphics defaults, fewer CPU
-- costs, a font that reads at this size (Nunito Black, OFL). The game's file is never
-- changed: love-mini makes these edits as the game loads.
local modules = {
  -- in the order PortMaster's patch script leaves them in main.lua
  "portmaster.text_cleanup", "portmaster.loc_fix", "portmaster.achievements", "portmaster.rumble",
  "portmaster.cpu_opt", "portmaster.particle_cleanup", "portmaster.options", "portmaster.controls",
  "portmaster.small_screen", "portmaster.perf",
}
local requires = {}
for _, m in ipairs(modules) do requires[#requires + 1] = 'require "' .. m .. '"' end

return {
  screen = "fit",
  -- Balatro plays with a gamepad (it shows its controller prompts and cursor) as long
  -- as no keys come: the Mini's buttons are the gamepad only
  keyboard = false,
  -- its swirling backgrounds are drawn by these shaders on any sprite (the logo's):
  -- without them, a flat background in their colour, not the sprite stretched
  shaders = {
    ["resources/shaders/background.fs"] = { effect = "flat", color = "colour_1" },
    ["resources/shaders/splash.fs"] = { effect = "flat", color = "colour_1" },
  },
  lua = "lua",
  env = {
    BALATRO_PM_PERF_OPTIMIZATIONS = "1",
    -- the Mini does not hold 60: an even 30 rather than an uneven 40-something
    BALATRO_PM_FPS_CAP = "30",
    BALATRO_PM_SKIP_RUMBLE = "1",
  },
  edits = {
    ["main.lua"] = {
      { 'require "challenges"', 'require "challenges"\n' .. table.concat(requires, "\n"), 1 },
    },
    -- the graphics defaults PortMaster's script sets: no CRT, bloom or shadows
    ["globals.lua"] = {
      { "crt = 70,", "crt = 0,", optional = true },
      { "bloom = 1", "bloom = 0", optional = true },
      { "shadows = 'On'", "shadows = 'Off'", optional = true },
    },
  },
  files = {
    ["resources/fonts/m6x11plus.ttf"] = "fonts/Nunito-Black.ttf",
  },
  -- the saves of the Balatro port love-mini takes over from (Producdevity's)
  saves_from = "/mnt/SDCARD/Saves/CurrentProfile/saves/Balatro",
  texture_budget_mb = 40,
}
